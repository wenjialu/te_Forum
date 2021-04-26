from django.shortcuts import render
from blocks.models import Block, Post, Comment, Likes
from blocks.forms import BlockForm, PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# Create your views here.
# 在首页展示界面上，按点赞数、阅读量分别展示推荐。在后台view函数中，需要将三种结果进行查询排序。
def index(request):
    # content = {}
    # form = CommentForm()
    # content["form"] = form
    return render(request, "index.html") 


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
    blocks = Block.objects.all()
    kmap["blocks"] = blocks  
    comment = Comment.objects.all()
    kmap["comment"] = comment
    likes = Likes.objects.all()         
    kmap["likes"] = likes   
    return render(request,"posts.html",kmap)    

# 为啥会重复保存之前post的表单内容？是之前的缓存吗？
@login_required
def addPost(request):
    print("addPost")
    if request.method == "POST":
        # print(request.POST)
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
    kmap["posts"] = posts 
    blocks = Block.objects.all()
    kmap["blocks"] = blocks   
    comment = Comment.objects.all()
    kmap["comment"] = comment
    likes = Likes.objects.all()
    kmap["likes"] = likes
    print("666")   
    return render(request,"posts.html",kmap)    

# 前端写一个表格，需要js： https://blog.csdn.net/wangjingna/article/details/51166499
# https://examples.bootstrap-table.com/ 
# https://mdbootstrap.com/docs/standard/plugins/table-editor/
# 我发现修改的代码和添加没啥大区别，就是新增的数据要先删掉再保存哦。
# 前端逻辑也改一改（前端modal 为editPage）。
@login_required
def editPost(request, id):
    print("editPost")
    if request.method == "POST":
        # 需要判断作者，只有原作者才能修改。
        post = Post.objects.get(id=id)
        oriAuthor =  post.author 
        thisAuthor = request.user 
        print(oriAuthor)    
        if oriAuthor == thisAuthor:
            form = PostForm(data = request.POST)
            if form.is_valid():
                print("form is valid")
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                # 所属的板块怎么获取，怎么设置？在前端用 select下拉框。注意名字对应。
                block_id = form.cleaned_data["block"]
                block = Block.objects.get(id = block_id)
                # 更新模型类
                # 还需要判断作者，只有原作者才能修改。
                
                post.title = title
                post.content = content
                post.block = block
                post.save()
                print("++++++++++valid & saved post++++++")
            print("error info （if any）", form.errors)
        else:
            return render(request,"notChange.html",kmap)     
    kmap = {}
    posts = Post.objects.all()
    kmap["posts"] = posts
    blocks = Block.objects.all()
    kmap["blocks"] = blocks 
    comment = Comment.objects.all()
    kmap["comment"] = comment
    likes = Likes.objects.all()         
    kmap["likes"] = likes    
    return render(request,"posts.html",kmap)    

@login_required
def delPost(request, id):
    print(delPost)
    if request.method == "POST":
        # 需要判断作者，只有原作者才能修改。
        post = Post.objects.get(id=id)
        oriAuthor =  post.author 
        thisAuthor = request.user 
        print(oriAuthor)    
        if oriAuthor == thisAuthor:
            post = Post.objects.get(id = id)
            print(post)
            # #数据库删除这条数据
            post.delete()
        else:
            return render(request,"posts.html",kmap)  
    kmap = {}
    posts = Post.objects.all()
    kmap["posts"] = posts 
    blocks = Block.objects.all()
    kmap["blocks"] = blocks 
    comment = Comment.objects.all()
    kmap["comment"] = comment   
    likes = Likes.objects.all()         
    kmap["likes"] = likes    
    return render(request,"posts.html",kmap)    

@login_required
def like_change(request, id):
    kmap = {}
    posts = Post.objects.all()
    kmap["posts"] = posts
    blocks = Block.objects.all()
    kmap["blocks"] = blocks 
    comment = Comment.objects.all()
    kmap["comment"] = comment           
    likes = Likes.objects.all()         
    kmap["likes"] = likes   
    if request.method == "POST":
        post = Post.objects.get(id = id)
        print(post.id)
        # 有就在基础上操作，如果没有就新建一个
        try:
            like = Likes.objects.get( post = int(id) )
            print("like.is_like",like.is_like)
            if like.is_like == True:
                like.is_like = False
                like.like_num -= 1
            else:
                like.is_like = True
                like.like_num += 1   
            like.save()                 
        except:
            like = Likes(id = id, post = post)
            print("yes")
            like.is_like = True
            like.like_num += 1  
            like.save() 
        print("like num", like.like_num)
        print("like.post",like.post)
        print("++++++++++saved like++++++")                     
    return render(request,"posts.html",kmap)    
