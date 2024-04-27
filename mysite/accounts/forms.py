from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'first_name', 'last_name', 'dob', 'hometown', 'gender')



class TagSearchForm(forms.Form):
    tags = forms.CharField(label='Search by Tags', max_length=100)

class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Search Users', max_length=100, required=False)

    def clean_search_query(self):
        data = self.cleaned_data['search_query'].strip()
        return data
    
class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True, label='Comment:')
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
        if commit:
            comment.save()
        return comment

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name'] 

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        album = super().save(commit=False)
        if not self.instance.pk:
            album.owner = self.user
        if commit:
            album.save()
        return album
    
class PhotoForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False, help_text="Enter comma-separated tags.")

    class Meta:
        model = Photo
        fields = ['album', 'caption', 'data']  

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['album'].widget = forms.HiddenInput()