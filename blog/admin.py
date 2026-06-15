from django.contrib import admin
from .models import Post , Comment
# Register your models here.
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['title','author','created','updated']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body','author','is_active',]