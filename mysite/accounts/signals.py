from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Album, Photo, Tag
from django.db.models import Count

@receiver(post_delete, sender=Album)
def cleanup_tags_after_album_deletion(sender, instance, **kwargs):
    check_and_delete_orphan_tags()

def check_and_delete_orphan_tags():
    # Check all tags to see if they are still associated with any photos.
    tags_with_counts = Tag.objects.annotate(photo_count=Count('photos'))
    for tag in tags_with_counts:
        if tag.photo_count == 0:
            tag.delete()