"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import *
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', home_view, name='home'),
    path('friends/', friends_view, name='friends'),
    path('search_results/', search_photos_by_tags, name='search_results'),
    path('photos/<str:tag_name>/', view_photos_by_tag, name='view_photos_by_tag'),
    path('photos/<str:tag_name>/all/', lambda request, tag_name: view_photos_by_tag(request, tag_name, True), name='view_all_photos_by_tag'),
    path('recommendations/', recommend_photos, name='photo-recommendations'),
    path('comments/', search_comments, name='comment_search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
