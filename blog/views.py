from django.shortcuts import render , get_object_or_404 ,redirect
from .models import Post
from .forms import CreatePostForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    return render (request ,'blog/index.html',{'posts':posts} )


def post_detail(request , pk):
    post = get_object_or_404(Post , pk=pk)
    return render(request,'blog/post_detail.html',{'post':post,'pk':pk})

@login_required
def create_post(request):
    # form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect ('blog:home')
    else :
        form = CreatePostForm()
    return render (request ,'blog/create_post.html',{'form':form ,'is_edit':False} )
@login_required
def update_post(request , pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user !=post.author:
        messages.error(request , "شما نمی توانید این پست را تغییر دهید")
        return redirect('home')
    if request.method == 'POST':
        form = CreatePostForm(request.POST , instance=post)
        if form.is_valid():
            form.save()
            messages.success(request , "پست با موفقیت تغییر یافت")
            return redirect ('blog:home')
    else:
        form=CreatePostForm(instance=post)
    return render (request ,'blog/create_post.html',{'form':form , 'is_edit':True})
        
@login_required
def delete_post(request , pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user != post.author:
        messages.error(request , "شما مجاز به حذف این پست نیستید")
        return redirect('blog:home')
    if request.method == 'POST':
        post.delete()
        messages.success(request , "پست با موفقیت حذف شد")
        return redirect('blog:home')
    return render(request , 'blog/post_delete_confirm.html',{'post':post})