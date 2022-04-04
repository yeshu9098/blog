from django import forms
from .models import Contact, Post

class MessageForm(forms.ModelForm):
    message = forms.Textarea()
    class Meta:
        model = Contact
        fields = ["message"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "category"]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'content'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
