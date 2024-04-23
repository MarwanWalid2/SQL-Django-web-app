from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import *
from .models import *
from django.http import HttpResponseRedirect

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

def home_view(request):
    photos = Photo.objects.all().order_by('-id')
    form = CommentForm(user=request.user if request.user.is_authenticated else None)

    if request.method == 'POST':
        if 'like_photo_id' in request.POST:
            photo_id = request.POST.get('like_photo_id')
            photo = get_object_or_404(Photo, id=photo_id)
            if request.user.is_authenticated:
                like, created = Like.objects.get_or_create(user=request.user, photo=photo)
            else:
                session_key = request.session.session_key or request.session.create()
                like, created = Like.objects.get_or_create(session_key=session_key, photo=photo)
            if not created:  # If the like already existed, remove it
                like.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif 'comment_photo_id' in request.POST:
            form = CommentForm(request.POST, user=request.user if request.user.is_authenticated else None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.photo = get_object_or_404(Photo, pk=request.POST.get('photo_id'))
                comment.save()
                return redirect('home')  # Refresh the page to clear the form and show the new comment

    return render(request, 'home.html', {'photos': photos, 'form': form})

# def like_photo(request, photo_id):
#     photo = Photo.objects.get(id=photo_id)
#     like, created = Like.objects.get_or_create(user=request.user, photo=photo)
#     if not created:  # If the like already existed, remove it
#         like.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# def like_photo(request, photo_id):
#     photo =  Photo.objects.get(Photo, id=photo_id)
#     if request.user.is_authenticated:
#         like, created = Like.objects.get_or_create(user=request.user, photo=photo)
#     else:
#         like, created = Like.objects.get_or_create(None, photo=photo)
#     if not created:  # If the like already existed, remove it
#         like.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
