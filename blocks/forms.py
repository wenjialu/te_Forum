from django import forms

# 外键第一次还是要设置的。
class BlockForm(forms.Form):
    title = forms.CharField(max_length=100)


# 外键和时间不用设定.设置一下除此之外的属性。  
class PostForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(min_length=1)
    block = forms.CharField(max_length=100)
       
class CommentForm(forms.Form):
    content = forms.CharField(min_length=1)
    
