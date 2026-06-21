from django import forms
from .models import Post , Comment , Profile , Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField( max_length=250, required=False,label='نام')
    last_name = forms.CharField( max_length=250, required=False ,label='نام خانوادگی')
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     # حذف help_text از همه فیلدها
        self.fields['password1'].help_text = None
    #     self.fields['password2'].help_text = None

class CreatePostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ("title",'body','status','category')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'placeholder': 'عنوان پست'
            }),
            'body': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'rows': 8,
                'placeholder': 'متن پست را اینجا بنویسید...'
            }),
            'category': forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
            'placeholder': 'عنوان کتگوری'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-white'
            }),
        }

class CommentForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    name = forms.CharField( max_length=158, required=False)
    class Meta:
        model = Comment
        fields = ('body',)

from django.contrib.auth.models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio',]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'placeholder': 'نام'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'placeholder': 'نام خانوادگی'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'placeholder': 'ایمیل'
            }),
        }