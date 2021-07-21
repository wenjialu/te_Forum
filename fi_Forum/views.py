from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect
from .models import Block,User,Reply,Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login

# Create your views here.
def index_register(request):
    if request.method == "POST":
        # 浏览器看下前端就知道前端需要填哪些值啦。
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not User.objects.filter(username=username).exists():
            #两次密码一致的话，就可以把用户注册信息存数据库啦。
            if password1 == password2:
                user = User(username = username)
                user.set_password(password1)
                user.save()
                messages.success(request, '注册成功')
                return redirect(to="login")
            else:
                messages.warning(request,"前后密码不一致")   
        else:
            messages.warning(request, "账号已存在")
    return render(request,"forum_register.html")                 

def index_login(request):
    # 只有这个函数是copy的。 不知道这个“next”是从哪来的，request里为啥会有这个。前端看了没有啊。
    next_url = request.GET.get("next")
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # 登录成功后，有下个页面的话，跳转到下一个页面
            if next_url:
                return redirect(next_url)
            # # 登录成功后。    
            return redirect("index")
        return HttpResponseRedirect(request.get_full_path()) #登录失败，依旧跳转到当前页面   
    #  还米有post的时候，渲染出login界面。
    return render(request, 'forum_login.html',{'next_url':next_url})   


def get_index(request):
    blocks = Block.objects.all()
    return render(request, "forum_index.html",{"plates":blocks})

def get_posts(request, id):
    if request.method == "GET":
        block = Block.objects.get(id=id)    
        return render(request, "forum_posts.html",{"plate":block})


# 不搞验证的form表单，逻辑清晰简单了好多哦！
@login_required
def post_post(request, id):
    if request.method == "POST":
        block = Block.objects.get(id=id)    
        title = request.POST.get("title")    
        content = request.POST.get("content")   
        post = Post(users = request.user, title = title, content = content, block = block)
        post.save()
        print(id)
        print("++++++++++ saved post++++++")
        messages.success(request, "帖子新建成功")
    # kmap = {}
    # posts = Post.objects.all()
    # kmap["posts"] = posts 
    # blocks = Block.objects.all()
    # kmap["blocks"] = blocks   
    # comment = Comment.objects.all()
    # kmap["comment"] = comment
    # likes = Likes.objects.all()
    # kmap["likes"] = likes
    # print("666")   
    # return redirect(to='block',id=id)
    return render(request,'forum_posts.html',{'plate':block})


def get_reply(request,id):
    reply = Post.objects.get(id=id)
    return render(request, "forum_article.html",{"article":reply})    


def put_post(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        #获取request的内容，用request的内容更新post。
        title = request.POST.get("title")
        content = request.POST.get("content")
        post.title = title
        post.content = content
        post.save()
        messages.success(request,"帖子修改成功")
    return redirect(to='reply',id=id)

def post_reply(request, id):
    if request.method == "POST":
        post = Post.objects.get(id=id)
        comment = request.POST.get("comment")
        reply = Reply.objects.create(user=request.user, post=post, content=comment)
        messages.success(request,"评论成功")
        # article = Post.objects.get(id=id)
    return redirect(to='reply',id=id)


def delete_reply(request, id):
    print("jinlaile")
    if request.method == "GET":
        reply = Reply.objects.get(id=id)
        print(reply,reply.post)
        post = reply.post
        print("=====")
        reply.delete()
        messages.success(request, '回复删除成功')
    # 删完了还是回到post-reply 的那个页面。
    # 回到post页面，id 得是post 的id，而不是reply的id。
    return redirect(to='reply',id=post.id)

# #删除帖子
def delete_post(request, id):
    if request.method == "GET":
        post = Post.objects.get(id=id)
        #在模型类里面可以看到他的字段。post有它对应的block的外键。
        block = post.block
        # print(post)
        print(post.block)
        #删贴
        post.delete()
        messages.success(request, '帖子删除成功')
    # 帖子删没了，就得回到他的板块block里去了。    
    return redirect(to='block',id=block.id)


# 权限 管理
# 板块有版主，帖子的删除功能由版主和帖子的创建者管理。回复的删除功能，也是由版主、帖子创建者和回复创建者进行操作。

# 在模板里面，可以判断用户身份和板块、帖子、评论之间的关系，再选择是否渲染修改和删除接口    