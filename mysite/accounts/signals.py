from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Photo, Tag
from django.db.models import Count

@receiver(pre_delete, sender=Photo)
def remove_orphaned_tags(sender, instance, **kwargs):
    tags_with_counts = Tag.objects.filter(photos=instance).annotate(photo_count=Count('photos'))
    for tag in tags_with_counts:
        if tag.photo_count == 0:
            tag.delete()