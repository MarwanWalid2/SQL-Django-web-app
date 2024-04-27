from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Friend)