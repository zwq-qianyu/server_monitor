"""auto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from monitor_app import views

urlpatterns = [
	# 后台管理路由
    url(r'^admin/', admin.site.urls),

    # 监控中心首页
    url(r'^$', views.index, name="index"),		#监控中心首页
    url(r'^(?P<pIndex>[0-9]+)$', views.index, name="list"), # 监控中心列表页
    url(r'^detail/(?P<gid>[0-9]+)$', views.detail, name="detail"), # 监控中心详情页
    url(r'^add$', views.add, name="add"),  #添加主机
    url(r'^delete$', views.delete, name="delete"),#删除相册信息
    url(r'^edit$', views.edit, name="edit"),#加载修改信息(编辑）

    # 用户登录和退出路由配置
    url(r'^login$', views.login, name="login"),
    url(r'^dologin$', views.dologin, name="dologin"),
    url(r'^logout$', views.logout, name="logout"),

    # 用户注册路由
    url(r'^register$', views.register, name="register"),
    url(r'^insert$', views.insert, name="insert"),
]
