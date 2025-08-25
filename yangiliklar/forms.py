from distutils.command.clean import clean

from django import forms

from .models import New,Users_info
from django.contrib.auth.forms import AuthenticationForm


class AddNewsForm(forms.ModelForm):
    class Meta:
        model=New
        fields=['title','descripton','image','category','author_id','status','is_trending']



class UpdateNews(forms.ModelForm):
    class Meta:
        model=New
        fields=['title','descripton','image','category','status','published_time','is_trending']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput,label='Parol')
    password_confirm = forms.CharField(widget=forms.PasswordInput,label='Parolni tasdiqlash')



    class Meta:
        model = Users_info
        fields = ["username" ,"password" ]

        labels = {
            "username" : "Foydalanuvchi nomi",
            "password" : "Parol"

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password !=password_confirm:
            raise forms.ValidationError("Parol mos kelmadi")
        return cleaned_data



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Foydalanuvchi Nomi')
    password = forms.CharField(widget=forms.PasswordInput,label='Parolni tasdiqlash')

