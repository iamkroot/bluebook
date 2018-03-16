from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    bio = forms.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'password1', 'password2']
