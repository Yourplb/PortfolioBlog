from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from .models import Profile
import os


@receiver(pre_delete, sender=Profile)
def delete_preview(sender, instance, **kwargs):
    if instance.photo.storage.exists(instance.photo.name):
        try:
            os.remove(instance.photo.path)
        except:
            pass
