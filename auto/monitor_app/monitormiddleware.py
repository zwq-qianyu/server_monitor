# 自定义中间件类
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

import re

class MonitorMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization(一次性配置和初始化).
        #print("ShopMiddleware")

    def __call__(self, request):
        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/login','/dologin','/logout','/register','/insert']
        # 获取当前请求路径
        path = request.path
        #print("Hello World!"+path)
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if path not in urllist:
            # 判断当前用户是否没有登录
            if "user" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('login'))


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response