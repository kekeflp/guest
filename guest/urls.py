"""guest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls.conf import include
from sign import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

# 添加路由, 规则 : url路径, 类.方法
urlpatterns = [
    # 系统自带管理路径
    # 优先使用url, 应为path不支持正则,,,,(重点掌握)
    url('admin/', admin.site.urls),
    # 自定义路径
    url(r'^index/$', views.index),
    url(r'^login_action/$', views.login_action),
    url(r'^event_manage/$', views.event_manage),
    # 页面反错时,跳转到首页
    url(r'^$', views.index),
    url(r'^accounts/login/$', views.index),
    url(r'^search_name/$', views.search_name),
    # 嘉宾页
    url(r'^guest_manage/$', views.guest_manage),
    url(r'^search_guest_name/$', views.search_guest_name),
    # 签到页面
    url(r'^sign_index/(?P<eid>[0-9]+)/$', views.sign_index),
    url(r'^sign_index_action/(?P<eid>[0-9]+)/$', views.sign_index_action),
    # 退出
    url(r'^logout/$', views.logout),
    # 
    # 以下是API
    # 
    url(r'^api/', include('sign.urls', namespace='sign')),
]
