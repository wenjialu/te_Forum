from django.shortcuts import render
from blocks.models import Block, Post, Comment
from blocks.forms import BlockForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.
@login_required
def addBlock(request):
    kmap = {}
    # blocks = Block.objects.all()
    # kmap["blocks"] = blocks
    if request.method == "POST":
        form = BlockForm(data = request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            print(type(request.user)) #<class 'django.utils.functional.SimpleLazyObject'>
            block = Block(banzhu = request.user,title = title
            )
            block.save()
            print("++++++++++valid & saved block++++++")
        print("error info （if any）", form.errors)
    return render(request,"block.html",kmap)    

@login_required
def getPosts(request):
    kmap = {}
    posts = Post.objects.all()
    kmap["posts"] = posts
    return render(request,"posts.html",kmap)    

# 表单没有保存成功呀
@login_required
def addPost(request):
    if request.method == "POST":
        form = PostForm(data = request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # 所属的板块怎么获取，怎么设置？
            post = Post(author = request.user,title = title, content = content, block = block)
            post.save()
            print("++++++++++valid & saved post++++++")
        print("error info （if any）", form.errors)
    kmap = {}
    posts = Post.objects.all()
    kmap["posts"] = posts    
    print("666")   
    return render(request,"posts.html",kmap)    
