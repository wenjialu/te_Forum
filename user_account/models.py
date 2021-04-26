from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
# Create your models here.
# 用户 系统默认
# #拓展User表格的方法，
# # 方法一：使用和用户模型一对一的链接(使用Profile扩展User模块)：
# 拓展：
#用户间关系：关注（粉丝）
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
    # 自带：password，username，email，date-joined
    # 好友
    friends = models.ForeignKey(to=User,related_name="friends", on_delete=models.CASCADE) 
    # (被关注)粉丝 一对多 foreignKey
    fans = models.ForeignKey(to=User,related_name="fans", on_delete=models.CASCADE) 
    # （主动关注）关注： 多对多 ManyToManyField

    #和User表做一对一关系画映射.  注意要加上on_delete
    user = models.OneToOneField(to=User, related_name="profile", on_delete=models.CASCADE)
    def __str__(self):
        return self.nickname



# 内容系统：
## 微博内容
class Weibo(models.Model):
    ## 转发微博 
    origin = models.CharField(max_length=100, default="")
    content = models.TextField(default="")
    author = models.ForeignKey(to=User,related_name="weibo_contents", on_delete=models.CASCADE) 
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)

## 评论
# 回复：回复的评论/回复[这个怎么写？？]，指定用户（不指定）
class Comment(models.Model):
    weibo = models.ForeignKey(to=Weibo,related_name="comments", on_delete=models.CASCADE) 
    author = models.ForeignKey(to=User,related_name="comments", on_delete=models.CASCADE) 
    content = models.TextField(default="") 
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    reply = models.ForeignKey(to=User,null=True,blank=True, on_delete=models.CASCADE)
    #  __str__ 设置展示在admin后台的是什么。
    def __str__(self):
        return self.author.username + self.content[:13]



