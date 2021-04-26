"""Forum URL Configuration

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
from blocks.views import index, addBlock, getPosts, addPost, editPost, delPost, like_change
from user_account.views import register, index_login

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'register/', register, name = "register"),
    path(r'login/', index_login, name = "login"),
    path(r'', getPosts),
    path(r'addBlock/', addBlock, name="addBlock"),
    path(r'getPosts/', getPosts, name="getPosts"),
    path(r'addPost/', addPost, name="addPost"),
    # path(r'editPost/', editPost, name="editPost"),
    path(r'editPost/<id>',editPost, name="editPost"),
    path(r'delPost/<id>',delPost, name="delPost"),
    path(r'like_change/<id>',like_change, name="like_change"),
    # 在django2.0之后，需要用re_path函数才适合正则匹配。 (?P<username>re)
    
]
