from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'dob', 'hometown', 'gender')


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)
    class Meta:
        model = Comment
        fields = ['text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        comment = super().save(commit=False)
        if self.user and self.user.is_authenticated:
            comment.user = self.user
        # Otherwise, the user will remain None and be treated as 'Guest' in display
        if commit:
            comment.save()
        return comment