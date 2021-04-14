from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
# Create your models here.
# 1. 用户模型
# 用户信息，除了django默认的基本属性，另外添加一个昵称nickname
class Profile(models.Model):
    nickname = models.CharField(max_length=128,default="很懒的一个用户")
    # gender 
    Gender = [
    (0, 'female'),
    (1, 'male')]
    gender = models.IntegerField(choices = Gender,default=0) 
    age = models.CharField(max_length=3,default="0")
    phone = models.CharField(max_length=11,default="1234566")
    address = models.CharField(max_length=256,default="用户很懒，没填写地址")
    abstract = models.TextField(default="用户很懒，没有描述")  
    #和User表做一对一关系画映射.  注意要加上on_delete
    user = models.OneToOneField(to=User, related_name="profile", on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname


# 自带user模型类里面的信息有：
# 但是它自带的User表，信息量却挺少的，有以下几个字段：

# username：账号

# password：密码

# FirstName和LastName：FirstName对应名，LastName对应姓氏，

# Email：邮箱

# Active：True or False，只有True才可以使用，Flase无法使用

# Staff status:True or False，为True可以登录到此Admin后台，False不行

# Superuser status：True or False，是否是超级管理员

# Last login：最后登录时间，每次登录都会更新

# Date joined：账户创建时间