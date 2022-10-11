from django import forms
# 
from .models import *


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs = {
                'rows': 4
            }
        )
    )
    class Meta:
        model = Comment
        fields = ('content',)