from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from .models import Post
import os


@receiver(pre_delete, sender=Post)
def delete_preview(sender, instance, **kwargs):
    if instance.preview.storage.exists(instance.preview.name):
        try:
            os.remove(instance.preview.path)
        except:
            pass
