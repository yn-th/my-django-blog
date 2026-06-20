from django.contrib import admin
from .models import Post , Comment , Profile , Category
# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created','updated']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body','author','is_active','parent']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)} 