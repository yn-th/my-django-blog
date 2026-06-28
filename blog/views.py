from django.shortcuts import render , get_object_or_404 ,redirect 
from .models import Post ,Comment , Profile , Category , Tag , Notification
from .forms import CreatePostForm , CommentForm ,ImageProfileForm, UserUpdateForm , ProfileForm ,CustomUserCreationForm
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .decorators import  group_required
from django.urls import  reverse
from django.contrib.auth.models import User
# Create your views here.

def signup(request):
    if request.method =='POST':
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request,"ثبت نام با موفقیت انجام شد ُاکنون میتوانید وارد شوید")
            return redirect('blog:home')
    else: 
        form = CustomUserCreationForm()
    return render(request,'blog/signup.html',{'form':form})

def post_list(request):
    post_list = Post.objects.filter(status=Post.Status.PUBLISH).order_by('-created')
    query = request.GET.get('q')
    if query:
        search_filter = Q(title__icontains = query) |Q(body__icontains = query)|Q(author__username__icontains = query)
        post_list = post_list.filter(search_filter)

    paginator = Paginator(post_list, 6)  # 6 پست در هر صفحه
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  # اگر شماره نامعتبر بود، صفحهٔ اول را می‌دهد

    return render(request, 'blog/index.html', {'posts': posts ,'query':query})

def category_posts(request , slug):
    category = get_object_or_404(Category,slug=slug)
    posts = category.posts.filter(status=Post.Status.PUBLISH).order_by('-created')
    query = request.GET.get('q')
    if query:
        search_filter = Q(title__icontains = query)|Q(body__icontains = query)
        posts = posts.filter(search_filter)
    paginator = Paginator(posts , 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)

    context = {
        'category':category,
        'quert':query,
        'posts':posts_page
    }
    return render(request , 'blog/category_posts.html',context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(
        is_active=True,
        parent=None,
        post=post
    )
    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(pk=request.user.pk).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        # تنظیم اجباری بودن فیلدها بر اساس لاگین بودن کاربر
        if request.user.is_authenticated:
            form.fields['name'].required = False
            form.fields['email'].required = False
        else:
            form.fields['name'].required = True
            form.fields['email'].required = True

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post

            # مدیریت پاسخ
            parent_id = request.POST.get('parent_id')
            if parent_id:
                # اطمینان از اینکه والد متعلق به همین پست است
                parent_comment = get_object_or_404(Comment, id=parent_id, post=post)
                new_comment.parent = parent_comment  

            # تنظیم نام و ایمیل
            if request.user.is_authenticated:
                new_comment.author = request.user
                # در صورت تمایل می‌توانید name و email را از پروفایل پر کنید
                new_comment.name = request.user.get_full_name() or request.user.username
                new_comment.email = request.user.email
            else:
                new_comment.name = form.cleaned_data['name']
                new_comment.email = form.cleaned_data['email']   

            new_comment.save()
            messages.success(request, "نظر شما با موفقیت ثبت شد و پس از تأیید نمایش داده می‌شود.")
            return redirect('blog:detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'is_liked':is_liked,
    })
    
@login_required
@group_required('Authors','Editors')
def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # if request.user.groups.filter(name = 'Authors').exists() and request.user.groups.filter(name = 'Editors').exists():
            #     post.status = Post.Status.REVIEW
            # else:
            #     post.status = Post.Status.PUBLISH
            if request.user.is_superuser or request.user.groups.filter(name='Editors').exists():
                pass  # وضعیت از فرم آمده، دست‌نخورده می‌ماند 

# اگر کاربر فقط Author باشد (و Editor نباشد)، وضعیت را به‌اجبار REVIEW می‌کنیم
            elif request.user.groups.filter(name='Authors').exists():
                post.status = Post.Status.REVIEW
                messages.info(request, "پست شما برای بررسی به ویراستار ارسال شد.")
            post.save()
            form.save_m2m()
            # ارسال اعلان به ویرایشگران
            if post.status == Post.Status.REVIEW:
                editors = User.objects.filter(
                    Q(groups__name='Editors') |Q(is_superuser=True)
            ).distinct()
    
                for editor in editors:
                    Notification.objects.create(
                        user=editor,
                        message=f"پست جدیدی برای بررسی: «{post.title}»",
                        link=reverse('blog:review_queue')  # یا می‌توانی لینک مستقیم به پست بدهی
        )
            return redirect ('blog:home')
    else :
        form = CreatePostForm()
    return render (request ,'blog/create_post.html',{'form':form ,'is_edit':False} )

@login_required
def update_post(request , pk):
    post = get_object_or_404(Post,pk=pk)
    if request.user !=post.author and not request.user.groups.filter(name = 'Editors').exsits() and not request.user.is_superuser:

        messages.error(request , "شما نمی توانید این پست را تغییر دهید")
        return redirect('home')
    if request.method == 'POST':
        form = CreatePostForm(request.POST ,request.FILES ,instance=post)
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
    if request.user != post.author and not request.user.groups.filter(name='Editors').exists() and not request.user.is_superuser:
        messages.error(request , "شما مجاز به حذف این پست نیستید")
        return redirect('blog:home')
    if request.method == 'POST':
        post.delete()
        messages.success(request , "پست با موفقیت حذف شد")
        return redirect('blog:home')
    return render(request , 'blog/post_delete_confirm.html',{'post':post})

@login_required
@group_required('Editors')
def review_queue(request):
    posts = Post.objects.filter(status = Post.Status.REVIEW).order_by('-created')
    return render (request , 'blog/review_queue.html',{'posts':posts})


@login_required
@group_required('Editors')
def approve_post(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.REVIEW)
    post.status = Post.Status.PUBLISH
    Notification.objects.create(
        user = post.author,
        message = f"پست {post.title}تایید و منتشر شد",
        link=reverse('blog:detail', args=[post.pk])

    )
    post.save()
    messages.success(request, "پست تأیید و به نویسنده اعلان فرستاده شد.")
    return redirect('blog:review_queue')

@login_required
@group_required('Editors')
def reject_post(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.REVIEW)
    post.status = Post.Status.DRAFT
    Notification.objects.create(
        user = post.author,
        message = f"پشت شما نیاز به ویرایش دارد{post.title}",
        link=reverse('blog:detail', args=[post.pk])
    )
    post.save()
    messages.success(request, "پست به پیش‌نویس برگشت داده شد.")
    return redirect('blog:review_queue')

@login_required
def notification_list(request):
    notifications = request.user.notification.all()

    # علامت‌گذاری همه به‌عنوان خوانده‌شده (با POST)
    if request.method == 'POST' and 'mark_all_read' in request.POST:
        notifications.filter(is_read=False).update(is_read=True)
        messages.success(request, "همهٔ اعلان‌ها خوانده شدند.")
        return redirect('blog:notification_list')

    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    notifications_page = paginator.get_page(page_number)

    return render(request, 'blog/notification_list.html', {
        'notifications': notifications_page
    })

@login_required
@group_required('Authors', 'Editors')
def dashboard(request):
    posts = Post.objects.filter(author= request.user).order_by('-updated')
    user = request.user
    is_editor = user.groups.filter(name='Editors').exists() or user.is_superuser
    is_author = user.groups.filter(name='Authors').exists() or is_editor 
    total = posts.count()
    published = posts.filter(status = Post.Status.PUBLISH).count()
    drafts = posts.filter(status = Post.Status.DRAFT).count()
    reviews = posts.filter(status=Post.Status.REVIEW).count()
    review_queue_count = 0
    if request.user.groups.filter(name='Editors').exists():
        review_queue_count = Post.objects.filter(status=Post.Status.REVIEW).count()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    context ={
        'posts':posts,
        'total':total,
        'published' : published,
        'drafts' : drafts,
        'reviews':reviews,
        'review_queue_count':review_queue_count,
        'is_editor':is_editor,
        'is_author':is_author,
    }

    return render(request , 'blog/dashboard.html',context)


@login_required
def post_liked(request , pk):
    post = get_object_or_404(Post,pk=pk)
    user= request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
        messages.success(request , 'شما این پست را پسندید')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # درخواست AJAX → ارسال JSON
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    else:
        # درخواست معمولی → ریدایرکت (fallback)
        return redirect('blog:detail', pk=post.pk)

# @login_required
# def my_profile(request ):
#     profile , create  = Profile.objects.get_or_create(user = request.user)
#     if request.method== 'POST':
#         if 'submit_user' in request.POST:

#             form_user = UserUpdateForm(request.POST, instance=request.user)
#             form_profile = ProfileForm(instance=profile)
#             if form_user.is_valid():
#                 form_user.save()
#                 messages.success(request,'پروفایل بروز شده')
#                 return redirect('blog:my_profile')
#         elif 'submit_profile' in request.POST:

#             form_user= UserUpdateForm(instance=request.user)
#             form_profile = ProfileForm(request.POST,instance=profile)
#             if form_profile.is_valid():
#                 form_profile.save()
#                 messages.success(request,'پروفایل بروز شدش')
#                 return redirect('blog:my_profile')
#         else:
#             form_user = UserUpdateForm(instance=request.user)
#             form_profile = ProfileForm(instance=profile)
#     else:
#         form_user = UserUpdateForm(instance=request.user)
#         form_profile = ProfileForm(instance=profile)

#     context = {
#         'form_user': form_user,
#         'form_profile': form_profile,
#         'profile': profile,
#     }      

#     return render(request , 'blog/profile.html',context)


@login_required
def my_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # اگر درخواست AJAX برای ذخیره فرم باشد (POST با form_type)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form_type = request.POST.get('form_type')

        if form_type == 'user_info':
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'اطلاعات حساب به‌روز شد.',
                    'data': {
                        'first_name': request.user.first_name,
                        'last_name': request.user.last_name,
                        'email': request.user.email,
                    }
                })
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        elif form_type == 'profile_bio':
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'بیوگرافی به‌روز شد.',
                    'data': {
                        'bio': profile.bio,
                    }
                })
        elif form_type == 'image':
            form = ImageProfileForm(request.POST,request.FILES ,instance=profile)
            if form.is_valid():
                form.save()
                return JsonResponse({
                'success':True,
                'messages':"عکس پروفایل بروز شد",
                'data':
                {
                    'image_url':profile.image.url
                }
            })


            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        return JsonResponse({'success': False, 'message': 'نوع فرم نامعتبر'})

    # GET معمولی
    form_user = UserUpdateForm(instance=request.user)
    form_profile = ProfileForm(instance=profile)
    form_image =ImageProfileForm(instance=profile)
    

    context = {
        'profile': profile,
        'form_user': form_user,
        'form_profile': form_profile,
        'form_image':form_image,
    }
    return render(request, 'blog/profile.html', context)

def tag_posts(request , slug):
    tag = get_object_or_404(Tag , slug = slug) 
    posts = tag.posts.filter(status = Post.Status.PUBLISH).order_by('-created')

    query = request.GET.get('q')
    if query:
        search_filter = Q(title__icontains = query)|Q(body__icontains = query)
        posts = posts.filter(search_filter)

    paginator= Paginator(posts , 6)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number) 

    context = {
        'tag':tag,
        'posts':posts,
        'query':query,

    }
    
    return render(request,'blog/tag_posts.html',context)

def about_us(request):
    return render(request,'blog/about.html')

def contact(request):
    return render(request,'blog/contact.html')