from django import forms
from django.contrib.auth.forms import AuthenticationForm
from frontend.models import Posts
from django.core.exceptions import ValidationError

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

class UserRegistrationForm(forms.Form):
    username = forms.CharField(
        required = True,
        label = 'Username',
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})  # Adding Bootstrap class
    )
    email = forms.CharField(
        required = True,
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})  # Adding Bootstrap class
    )
    password = forms.CharField(
        required = True,
        label = 'Password',
        max_length = 32,
        widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        
    )



# class MovieForm(forms.Form):
#     def __init__(self, *args, **kwargs):

class MovieForm(forms.Form):
   
    name = forms.CharField(max_length=100, required=True)
    image = forms.CharField(required=True)
    rate = forms.DecimalField(required=True)
    size = forms.DecimalField(required=True)
    genre = forms.CharField(required=True)
    lang = forms.CharField(required=True)
    story = forms.CharField(required=True)