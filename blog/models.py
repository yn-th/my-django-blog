from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.

class Tag(models.Model):
    name = models.CharField( max_length=250)
    slug = models.SlugField(allow_unicode=True)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name , allow_unicode=True)
        super(Tag,self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name'] 


class Category(models.Model):
    name = models.CharField( max_length=250)
    slug = models.SlugField(allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        
    def save(self ,*args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name,allow_unicode=True)
        super(Category, self).save(*args, **kwargs)
    def __str__(self):
        return self.name



class Post (models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    image = models.ImageField(upload_to='posts/%Y/%m', blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts',blank=True)
    category = models.ForeignKey(
        Category,
        related_name="posts",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
        )
    
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
    likes = models.ManyToManyField(
        User,
        related_name='liked_post',
        blank=True,
        )
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


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField( upload_to='profile/%Y/%m', blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
    
