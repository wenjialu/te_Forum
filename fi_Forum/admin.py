from django.contrib import admin
from .models import User, Block, Post, Reply
# Register your models here.



admin.site.register(User)
admin.site.register(Block)
admin.site.register(Post)
admin.site.register( Reply)