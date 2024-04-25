from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.forms import *
from accounts.models import *
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q



def home_view(request):
    albums = Album.objects.all().prefetch_related('photos') 
    form = CommentForm(user=request.user if request.user.is_authenticated else None)
    searchform = TagSearchForm(request.GET or None)
    tags = Tag.objects.annotate(photo_count=models.Count('photos')).order_by('-photo_count')[:10]

    if request.method == 'POST':
        if 'like_photo_id' in request.POST:
            photo_id = request.POST.get('like_photo_id')
            photo = get_object_or_404(Photo, id=photo_id)
            if request.user.is_authenticated:
                like, created = Like.objects.get_or_create(user=request.user, photo=photo)
            else:
                if not request.session.session_key:
                    request.session.save() 
                session_key = request.session.session_key
                print(session_key)
                like, created = Like.objects.get_or_create(session_key=session_key, photo=photo)
            if not created:
                like.delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        elif 'comment_photo_id' in request.POST:
            form = CommentForm(request.POST, user=request.user if request.user.is_authenticated else None)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.photo = get_object_or_404(Photo, pk=request.POST.get('photo_id'))
                comment.save()
                return redirect('home')  # Refresh the page to clear the form and show the new comment

    return render(request, 'home.html', {
        'albums': albums,
        'form': form,
        'searchform': searchform,
        'tags': tags
    })


User = get_user_model()
@login_required
# views.py

def friends_view(request):
    form = UserSearchForm(request.GET or None)
    search_results = []
    friends = set()

    # Get the current user's friends
    friends_relations = Friend.objects.filter(Q(user1=request.user) | Q(user2=request.user))
    friend_ids = {relation.user2.id if relation.user1 == request.user else relation.user1.id for relation in friends_relations}
    for relation in friends_relations:
        friends.add(relation.user2 if relation.user1 == request.user else relation.user1)

    if 'search' in request.GET and form.is_valid():
        search_query = form.cleaned_data['search_query']
        search_results = User.objects.filter(
            Q(email__icontains=search_query) & 
            ~Q(id__in=friend_ids) &  # Exclude current friends
            ~Q(id=request.user.id)  # Exclude the current user themselves
        )

    if 'add_friend' in request.POST:
        friend_id = request.POST.get('add_friend')
        friend_user = User.objects.get(pk=friend_id)
        Friend.objects.get_or_create(user1=request.user, user2=friend_user)  # Changed to get_or_create to avoid duplicates
        return redirect('friends')

    return render(request, 'friends.html', {
        'form': form,
        'search_results': search_results,
        'friends': friends
    })


def search_photos_by_tags(request):
    tags = []
    if request.method == 'GET' and 'tags' in request.GET:
        tag_names = request.GET['tags'].split()
        tags = Tag.objects.filter(name__in=tag_names)
    return render(request, 'search_results.html', {'tags': tags})



def view_photos_by_tag(request, tag_name):
    form = CommentForm(user=request.user if request.user.is_authenticated else None)
    tag = Tag.objects.get(name=tag_name)
    view_all = 'view_all' in request.GET
    view_mine = 'view_mine' in request.GET
    error_message = None

    if view_all:
        photos = tag.photos.all()
    elif view_mine:
        #check if the user is registered if so then show only their photos
        if request.user.is_authenticated:
            photos = tag.photos.filter(album__owner=request.user)
        else:
            error_message = "You need to be registered to view your photos"
            photos = tag.photos.none()
    else:
        photos = tag.photos.all()
        
    return render(request, 'photos_by_tag.html', {'photos': photos, 'tag_name': tag_name, 'error_message': error_message, 'form': form,})