from django.db import models
from django.contrib.auth.models import User, AbstractUser
import datetime
# Create your models here.

# 2. 板块模型
# 板块模板，基础属性有标题title、对应版主users，只有两个属性
class Block(models.Model):
    title = models.CharField(max_length=100, default="")
    banzhu = models.ForeignKey(to=User,related_name="blocks", on_delete=models.CASCADE) 
    def __str__(self):
        return self.title
 

# 3. 帖子模型
# 帖子模型，基础属性有标题title、内容content，还有个创建者user和创建时间createtime和板块Block，总共5个属性
class Post(models.Model):
    title = models.CharField(max_length=100, default="")
    author = models.ForeignKey(to=User,related_name="posts", on_delete=models.CASCADE) 
    content = models.TextField(default="")
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    block =  models.ForeignKey(to=Block,related_name="posts", on_delete=models.CASCADE) 
     #  __str__ 设置展示在admin后台的是什么。
    def __str__(self):
        return self.title

# 4. 回复模型
# 回复模型，属性有创建者user，评论comment，创建时间createtime以及回复的帖子post，共4个属性
class Comment(models.Model):
    author = models.ForeignKey(to=User,related_name="comments", on_delete=models.CASCADE) 
    content = models.TextField(default="") 
    create_time = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now)
    reply = models.ForeignKey(to=Post,null=True,related_name="comments", on_delete=models.CASCADE)
    #  __str__ 设置展示在admin后台的是什么。
    def __str__(self):
        return self.author.username + self.content[:13]