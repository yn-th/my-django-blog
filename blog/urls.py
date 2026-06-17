from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.post_list,name='home'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('create/',views.create_post,name='create'),
    path('profile/',views.my_profile , name='my_profile'),
    path('detail/like/<pk>',views.post_liked,name='like_post'),
    path('detail/<pk>',views.post_detail,name='detail'),
    path('edit/<pk>',views.update_post,name='edit'),
    path('delete/<pk>',views.delete_post,name='delete'),

]
