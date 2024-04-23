from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('album/<int:album_id>/delete/', views.delete_album, name='delete_album'),
]
