from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment
from django.utils.translation import ugettext_lazy as _


class SignUpForm(UserCreationForm):
    bio = forms.CharField(max_length=500)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'password1', 'password2']


class AddFavorite(forms.Form):
    """Add post to user's favorites."""
    fav = forms.BooleanField(required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': _('Add comment')
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'style': 'resize:none;'
            })
        }
