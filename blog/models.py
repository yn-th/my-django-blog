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