from django import forms
from django.contrib.auth.models import User
from grumblr.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20)
    firstname = forms.CharField(max_length = 20)
    lastname = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 200)
    password2 = forms.CharField(max_length = 200)
    email = forms.EmailField(max_length = 100)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email is already taken.")

        return email

class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    age = forms.IntegerField()
    bio = forms.CharField(max_length=420)
    picture = forms.ImageField(required=False)
    
    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        
        return cleaned_data
    
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if not type(age) is int:
            raise forms.ValidationError("Age must be an integer.")
        if not age >= 0:
            raise forms.ValidationError("Age must be a positive integer.")

        return age

class ChangeForm(forms.Form):
    oldpassword = forms.CharField(max_length=200) 
    password = forms.CharField(max_length = 200)
    password2 = forms.CharField(max_length = 200)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ChangeForm, self).clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data
    
    def clean_oldpassword(self):
        oldpassword = cleaned_data.get('oldpassword')
        if not self.user.check_password(oldpassword):
            raise forms.ValidationError("OldPasswords is not correct.")

        return oldpassword

class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length = 200)
    password2 = forms.CharField(max_length = 200)
    
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords did not match.")

        return cleaned_data
    
class ResetForm(forms.Form):
    email = forms.EmailField(max_length = 100)

    def clean(self):
        cleaned_data = super(ResetForm, self).clean()
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email):
            raise forms.ValidationError("Email not registered.")

class PostForm(forms.Form):
    text = forms.CharField(max_length = 42)
    
    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        text = self.cleaned_data.get('text')

        return cleaned_data