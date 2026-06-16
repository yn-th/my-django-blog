from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post (models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Status(models.TextChoices):
        DRAFT = 'DF','پیش نویس'
        PUBLISH = 'PB','منتشر شده'
    
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default= Status.DRAFT,
        )
    def __str__(self):
        return f"{self.title} - {self.author}"
    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_comments',
        blank=True,
        null=True
        )
    parent = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        blank=True,
        null=True
        )
    name = models.CharField( max_length=150, blank=True)
    email = models.EmailField(max_length=254,blank=True)
    body = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
        )
    created = models.DateTimeField( auto_now_add=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"کامنت {self.author} روی {self.post.title[:30]}"