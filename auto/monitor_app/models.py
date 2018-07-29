from django.db import models
from datetime import datetime

# 用户信息模型
class Users(models.Model):
    username = models.CharField(max_length=32)   # 唯一性约束
    password = models.CharField(max_length=32)
    addtime = models.DateTimeField(default=datetime.now)

    def toDict(self):
        return {'id':self.id,'username':self.username,'password':self.password}

    class Meta:
        db_table = "users"  # 更改表名

# 主机信息模型
class Host(models.Model):
    uid = models.CharField(max_length=32)   #登录用户的用户名
    host_user = models.CharField(max_length=32)   # 唯一性约束
    host_password = models.CharField(max_length=32)
    tag = models.CharField(max_length=32)
    ip = models.CharField(max_length=32)
    cpu = models.IntegerField()
    vir_mem = models.IntegerField()
    mem = models.IntegerField()
    host_status = models.CharField(max_length=32)
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "host"  # 更改表名

# 主机实时信息模型
class Monitor(models.Model):
    host_id = models.CharField(max_length=32)   #登录用户的用户名
    cpu_used = models.CharField(max_length=32)
    vir_mem_used = models.CharField(max_length=32)
    mem_used = models.CharField(max_length=32)
    addtime = models.DateTimeField(default=datetime.now)

    class Meta:
        db_table = "monitor"  # 更改表名
