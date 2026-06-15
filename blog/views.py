from django.shortcuts import render , get_object_or_404 ,redirect
from .models import Post ,Comment
from .forms import CreatePostForm , CommentForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    return render (request ,'blog/index.html',{'posts':posts} )


def post_detail(request , pk):
    post = get_object_or_404(Post , pk=pk)
    comments = Comment.objects.filter(is_active = True)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if request.user.is_authenticated:
            form.fields['name'].required=False
            form.fields['email'].required=False
        else:
            form.fields['name'].required=True
            form.fields['email'].required=True

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            if request.user.is_authenticated:
                new_comment.author = request.user
            else:
                new_comment.name = form.cleaned_data['name']
                new_comment.name = form.cleaned_data['email']

            new_comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد و پس از تأیید نمایش داده می‌شود.")
            return redirect('blog:detail',pk = post.pk)
        
    else:
        form = CommentForm()

    return render(request,'blog/post_detail.html',{'post':post,'pk':pk,'comments':comments,'form':form})

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

@login_required
def dashboard(request):
    posts = Post.objects.filter(author= request.user).order_by('-updated')
    total = posts.count
    published = posts.filter(status = Post.Status.PUBLISH).count
    drafts = posts.filter(status = Post.Status.DRAFT).count

    context ={
        'posts':posts,
        'total':total,
        'published' : published,
        'drafts' : drafts
    }

    return render(request , 'blog/dashboard.html',context)

