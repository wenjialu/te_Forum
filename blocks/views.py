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

# 为啥会重复保存之前post的表单内容？是之前的缓存吗？
@login_required
def addPost(request):
    print("addPost")
    if request.method == "POST":
        print(request.POST)
        # 多加一层 PostForm 是为了实现验证功能吗？
        form = PostForm(data = request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            # 所属的板块怎么获取，怎么设置？在前端用 select下拉框。注意名字对应。
            block_id = form.cleaned_data["block"]
            block = Block.objects.get(id = block_id)
            post = Post(author = request.user,title = title, content = content, block = block)
            post.save()
            print("++++++++++valid & saved post++++++")
        print("error info （if any）", form.errors)
    kmap = {}
    posts = Post.objects.all()
    blocks = Block.objects.all()
    # print("blocks", blocks)
    kmap["posts"] = posts 
    kmap["blocks"] = blocks   
    print("666")   
    return render(request,"posts.html",kmap)    

# 前端写一个表格，需要js： https://blog.csdn.net/wangjingna/article/details/51166499
# https://examples.bootstrap-table.com/ 
# https://mdbootstrap.com/docs/standard/plugins/table-editor/
@login_required
def editPost(request):
    return