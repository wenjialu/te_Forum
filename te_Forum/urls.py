"""second_Forum URL Configuration

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
from django.contrib import admin
from django.urls import path, re_path
from fi_Forum.views import get_index, get_posts,post_post,get_reply,post_reply,delete_reply,put_post,delete_post
from fi_Forum.views import index_login,index_register

## 在django2.0之后，需要用re_path函数才适合正则匹配。 (?P<username>re)
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^index/$',get_index, name="index"),
    re_path(r'^block/(?P<id>\d+)/$',get_posts,name='block'),
    re_path(r'^block/(?P<id>\d+)/post/$',post_post),
    re_path(r'^reply/(?P<id>\d+)/$',get_reply,name='reply'),
    re_path(r'^reply/(?P<id>\d+)/comment/$',post_reply),
    re_path(r'^reply/(?P<id>\d+)/comment/delete/$',delete_reply),
    re_path(r'^reply/(?P<id>\d+)/put/$',put_post),
    re_path(r'^reply/(?P<id>\d+)/delete/$',delete_post),
    path(r'login/', index_login, name="login"),
    path(r'register/', index_register, name="register"),
]