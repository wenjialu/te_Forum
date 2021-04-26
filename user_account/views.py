from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import login
import json
# Create your views here.
# 用户系统
##注册
##登录

#form 遇到问题查官方文档，比查乱七八糟的教程有用&快的多了
def register(request):
    if request.method == "GET":
        form  = UserCreationForm()
    if request.method == "POST":
        form  = UserCreationForm(request.POST)
        print(request.POST)
        # print("form",form) #发现我的请求没有传到我的表单里面去诶。所以form.is_valid=False.
        # is_valid 不仅判断 表单是否存在，主要会判断是否符合规范，比如至少8个字符，包含字母等。
        print(form.is_valid())
        # https://docs.djangoproject.com/en/3.1/topics/forms/modelforms/ 
        print(form.errors) # 我怎么知道这个form还有哪些属性，看官方文档 UserCreationForm()或者他的父类forms.ModelForm which are a django forms里面有哪些字段
        if form.is_valid():
            print("开始保存表单")
            form.save()
            print("表单保存成功")
            return redirect(to = "login")
    
    content = {}
    content["status"] = "register"
    content["form"] = form         
    return render(request,"clean_index.html",content)


# 注意函数起名不要起login啊，和  Django 自带的login 冲突了。
def index_login(request):
    # 如果是简单的GET请求，只需要初始化登录的表单，然后传到前端进行渲染
    if request.method == "GET":
        form = AuthenticationForm()
# 如果是POST请求，使用AuthenticationForm接收post参数，并进行验证，验证通过，进行登录处理。        
    if request.method == "POST":
        #  @login_required 装饰器配置.记录下下个url，方便把登录信息传过去？
        next_url = request.GET.get("next")
        print("next url", next_url)
        # 注意： 这里传参一定要传给 data ！！！！！
        form = AuthenticationForm(data = request.POST)  
        print(form.is_valid(),form.error_messages)
        if form.is_valid():
            print(form.get_user())
            login(request, form.get_user())
            # return HttpResponse("Login Success")
            if next_url:
                return redirect(to=next_url)
            # return HttpResponse("Login Success")    
            return redirect(to="homepage")        
    content = {}
    content["form"] = form 
    content["status"] = "login"
    return render(request,"clean_index.html",content)

