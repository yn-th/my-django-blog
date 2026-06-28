from django.urls import path , reverse_lazy
from . import views
from django.contrib.auth.views import LoginView , LogoutView 
app_name = 'blog'
from django.contrib.auth import views as auth_views

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views


urlpatterns = [
#   path('password-reset/',
#          auth_views.PasswordResetView.as_view(template_name='blog/password_reset_form.html',success_url=reverse_lazy('blog:password_reset_done') ),
#          name='password_reset'),
#     path('password-reset/done/',
#          auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),
#          name='password_reset_done'),
#     path('password-reset-confirm/<uidb64>/<token>/',
#          auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html',success_url=reverse_lazy('blog:password_reset_complete') ),
#          name='password_reset_confirm'),
#     path('password-reset-complete/',
#          auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),
#          name='password_reset_complete'),

    path('',views.post_list,name='home'),
    path('about/',views.about_us,name='about'),
    path('contact/',views.contact,name='contact'),
    path('signup',views.signup,name='signup'),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('create/',views.create_post,name='create'),
    path('profile/',views.my_profile , name='my_profile'),
    path('detail/like/<pk>',views.post_liked,name='like_post'),
    path('detail/<pk>',views.post_detail,name='detail'),
    path('edit/<pk>',views.update_post,name='edit'),
    path('delete/<pk>',views.delete_post,name='delete'),
    path('tags/<slug>',views.tag_posts,name='tag_posts'),
    path('review-queue/', views.review_queue, name='review_queue'),
    path('approve/<int:pk>/', views.approve_post, name='approve_post'),
    path('reject/<int:pk>/', views.reject_post, name='reject_post'),
    
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('notifications/', views.notification_list, name='notification_list'),
]


urlpatterns += [
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='blog/password_reset_form.html',
             success_url=reverse_lazy('blog:password_reset_done')
         ),
         name='password_reset'),
         
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='blog/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='blog/password_reset_confirm.html',
             success_url=reverse_lazy('blog:password_reset_complete')
         ),
         name='password_reset_confirm'),
         
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='blog/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]