from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})




def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('accounts:login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('accounts:login') 


@login_required
def profile_view(request):
    albums = Album.objects.filter(owner=request.user).prefetch_related('photos')
    form = AlbumForm(user=request.user)
    photo_form = PhotoForm()  # Initialize the photo form
    photo_form.fields['album'].queryset = albums  # Limit album choices to user's own albums

    if request.method == 'POST':
        if 'create_album' in request.POST:
            form = AlbumForm(request.POST, user=request.user)
            if form.is_valid():
                form.save()
                return redirect('accounts:profile')
        elif 'upload_photo' in request.POST:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                photo_form.save()
                return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'form': form, 'photo_form': photo_form, 'albums': albums})

@login_required
def delete_album(request, album_id):
    album = get_object_or_404(Album, id=album_id, owner=request.user)  # Ensure the user owns the album
    if request.method == 'POST':
        album.delete()
        return redirect('accounts:profile')  # Redirect to the profile page or wherever appropriate
    return redirect('accounts:album_detail', album_id=album_id)

