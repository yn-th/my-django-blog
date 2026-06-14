from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.post_list,name='home'),
    path('create/',views.create_post,name='create'),
    path('detail/<pk>',views.post_detail,name='detail'),
    path('edit/<pk>',views.update_post,name='edit'),
    path('delete/<pk>',views.delete_post,name='delete'),

]
