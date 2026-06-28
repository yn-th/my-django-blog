from django import forms
from .models import Post , Comment , Profile , Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_quill.forms import QuillFormField
from django_quill.widgets import QuillWidget 

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
        fields = ("title",'status','category','tags','image')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition',
                'placeholder': 'عنوان پست'
            }),
            'body': forms.Textarea(attrs={
                'id': 'quill-textarea',  # یک ID ثابت برای دسترسی JavaScript
                'class': 'hidden',       # با Tailwind مخفی می‌شود
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-white'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-white'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition bg-white',
                'size': '5'  # ارتفاع لیست (اختیاری)
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
        })
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
        fields = ['bio']

class ImageProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
            }),
        }
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