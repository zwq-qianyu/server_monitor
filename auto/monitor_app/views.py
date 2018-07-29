from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from datetime import datetime
from .models import Users, Host, Monitor
import json, psutil
import os
import paramiko
import re

# 公共信息加载函数
def loadinfo(request):
    lists = Host.objects.filter()
    context = {'hostlist':lists}
    return context

def index(request, pIndex=1):
    '''监控中心列表页'''
    context = loadinfo(request)
    #查询主机信息
    mod = Host.objects
    mywhere = []
    #判断封装搜索条件
    tid = int(request.GET.get("tid",0))
    if tid > 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append('tid='+str(tid))
    else:
        list = mod.filter()

    #执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 5) #以5条每页创建分页对象
    maxpages = page.num_pages #最大页数
    #判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex) #当前页数据
    plist = page.page_range   #页码数列表

    #封装模板中需要的信息
    context['username'] = request.session['user']['username']
    context['id'] = request.session['user']['id']
    context['hostlist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['mywhere'] = mywhere
    return render(request,"index.html",context)

def delete(request):
    try:
        #找到对应的主机对象
        if request.method == "POST":
            host_id = request.POST.get('id')
        ob = Host.objects.get(id=host_id)
        ob.delete()
        return HttpResponse(json.dumps({
                "code": 0,
                "msg": "删除成功"
            }))
    except Exception as e:
        return HttpResponse(json.dumps({
                "code": 1,
                "msg": "删除失败"
            }))

def edit(request):
    try:
        if request.method == "POST":
            host_id = request.POST.get('id')
            ob = Host.objects.get(id=host_id)
            print(ob.tag)
            ob.tag = request.POST.get('new_tag')
            ob.save()
            print(ob.tag)
        return HttpResponse(json.dumps({
                "code": 0,
                "msg": "修改成功"
            }))
    except Exception as e:
        return HttpResponse(json.dumps({
                "code": 1,
                "msg": "修改失败"
            }))

def detail(request,gid):
    '''主机详情页'''
    context = loadinfo(request)
    mo = Monitor.objects.get(host_id=gid)
    ob = Host.objects.get(id=gid)
    # 远程主机上执行命令
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
    ssh.connect(hostname=ob.ip, username=ob.host_user, password=ob.host_password, port=22)
    print("建立ssh连接")
    command = "cd /tmp && python3 /tmp/timely_monitor.py"
    stdin, stdout, stderr = ssh.exec_command(command)
    print("command执行完成")
    strs = stdout.read().decode()
    print(strs)
    cpu_str = re.findall(r'{.*?cpu_percent":.(.*?),.*?\n',strs)
    if cpu_str == []:
        cpu_str = re.findall(r'{.*?cpu_percent":.(.*?)}\n',strs)
    print(cpu_str)
    print(cpu_str[0])
    cpu = [0,0,0,0,0,0,0,0,0,0]
    for i in range(0, len(cpu_str)):
        cpu[i] = float(cpu_str[i])
    print(cpu)
    vir_mem_str = re.findall(r'{.*?memory_percent":.(.*?),.*?\n',strs)
    if vir_mem_str == []:
        vir_mem_str = re.findall(r'{.*?memory_percent":.(.*?)}\n',strs)
    print(vir_mem_str)
    vir_mem = [0,0,0,0,0,0,0,0,0,0]
    for i in range(0, len(cpu_str)):
        vir_mem[i] = float(vir_mem_str[i])
    print(vir_mem)

    ssh.close()

    # mo.cpu_used = res['cpu_percent']
    # mo.vir_mem_used = res['memory_percent']
    # mo.mem_used = res['disk_percent']
    # mo.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # ob.save()
    # mo.save()
    context['cpu_percent'] = cpu_str[4]
    context['vir_mem_used'] = vir_mem_str[4]
    context['mem_used'] = mo.mem_used
    context['cpu_data'] = cpu
    context['vir_mem_data'] = vir_mem
    return render(request,"detail.html",context)

def add(request):
    '''添加主机'''
    try:
        print("添加主机中")
        ob = Host()
        if request.method == "POST":
            ob.uid = request.POST.get('id')
            ob.host_user = request.POST.get('username')   
            ob.host_password = request.POST.get('password')
            ob.tag = request.POST.get('tag')
            ob.ip = request.POST.get('ip')
            print(ob.host_user)
            #print(ob.host_password)
            print(ob.ip)

            # 远程文件传输
            transport = paramiko.Transport((ob.ip, 22))
            transport.connect(username=ob.host_user, password=ob.host_password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            print("已连接到主机中")
            # 上传到远程主机
            print("当前目录：" + str(os.getcwd()))
            sftp.put('./static/monitor.py', '/tmp/monitor.py')
            sftp.put('./static/timely_monitor.py', '/tmp/timely_monitor.py')
            sftp.close()
            transport.close()
            print("传输完成")

            # 远程主机上执行命令
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 允许连接不在know_hosts文件中的主机
            ssh.connect(hostname=ob.ip, username=ob.host_user, password=ob.host_password, port=22)
            print("建立ssh连接")
            stdin,stdout,stderr = ssh.exec_command("pip3 install psutil")
            out,err = stdout.read(),stderr.read()
            if err:
              print(err)
            else:
              print(out)
            command = "python3 /tmp/monitor.py && rm -f /tmp/monitor.py"
            stdin, stdout, stderr = ssh.exec_command(command)
            print("command执行完成")
            strs = stdout.read()
            #print(strs)
            res = json.loads(strs.decode('utf-8'))   #将字符串转为json格式
            print(strs)

            ssh.close()
            mo = Monitor()
            ob.cpu = res["cpu_count"]
            # print("dfaga")
            mo.cpu_used = res['cpu_percent']
            ob.vir_mem = res['memory_total']
            mo.vir_mem_used = res['memory_percent']
            ob.mem = res['disk_total']
            mo.mem_used = res['disk_percent']
            ob.host_status = 'running'
            ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mo.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            print("保存数据到数据库")
            ob.save()
            mo.host_id = ob.id;
            mo.save()
            print("已成功保存数据到数据库")
            return HttpResponse(json.dumps({
                "code": 0,
                "msg": "添加成功",
                "data": {
                    'id': ob.id,
                    'cpu': ob.cpu,
                    'vir_mem': ob.vir_mem,
                    'mem': ob.mem,
                    'status': ob.host_status
                }
            }))
    except Exception as err:
        print(err)
        return HttpResponse(json.dumps({
            "code": 1,
            "msg": "添加失败",
            "data": {}
        }))

# ==============前台会员登录====================
def login(request):
    '''会员登录表单'''
    return render(request,'login.html')

def dologin(request):
    '''会员执行登录'''
    ''' # 校验验证码
    verifycode = request.session['verifycode']
    code = request.POST['code']
    if verifycode != code:
        context = {'info':'验证码错误！'}
        return render(request,"login.html",context)
    '''
    try:
        #根据账号获取登录者信息
        user = Users.objects.get(username=request.POST['username'])
        #判断当前用户是否是后台管理员用户
        # 验证密码
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        if user.password == m.hexdigest():
            # 此处登录成功，将当前登录信息放入到session中，并跳转页面
            print("登录成功")
            request.session['user'] = user.toDict()
            return redirect(reverse('index'))
        else:
            context = {'info':'登录密码错误！'}
    except:
        context = {'info':'登录账号错误！'}
    return render(request,"login.html",context)

def logout(request):
    '''会员退出'''
    # 清除登录的session信息
    del request.session['user']
    # 跳转登录页面（url地址改变）
    return redirect(reverse('login'))

# ==============前台会员注册====================
def register(request):
    '''加载会员注册页面'''
    return render(request,"register.html")

def insert(request):
    '''执行会员信息添加'''
    try:
        ob = Users()
        ob.username = request.POST['username']
        #获取密码并md5
        import hashlib
        m = hashlib.md5() 
        m.update(bytes(request.POST['password'],encoding="utf8"))
        ob.password = m.hexdigest()
        # ob.password = request.POST['password']
        ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"注册成功！"}
        return render(request,"login.html",context)
    except Exception as err:
        print(err)
        context={"info":"注册失败"+str(err)}
        return render(request,"register.html",context)
    

'''
def verify(request):
    #引入随机函数模块
    print("进入verify")
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('../static/font/msyh.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'img/png')
'''
