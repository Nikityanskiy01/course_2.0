from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ProductReview
from django import forms

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Your nickname here'}
        ))
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Your password here'}
        ))

    password2 = forms.CharField(label='Password again', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Your password again'}
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-input', 'placeholder': 'Your nickname here'}
        ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-input', 'placeholder': 'Your password here'}
        ))


class ReviewForm(forms.ModelForm):
    content = forms.CharField(label='Content',  widget=forms.Textarea(
        attrs={'class': 'review-text', 'maxlength': '2048'}
        ), required=True)
    is_recommend = forms.BooleanField(label='Will you recommend?', initial=True, required=False)

    class Meta:
        model = ProductReview
        fields = ['content', 'is_recommend']