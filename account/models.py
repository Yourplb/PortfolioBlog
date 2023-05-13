from django.db import models
from django.conf import settings
# Create your models here.


class Profile(models.Model):
    objects = None
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    about_user = models.TextField(blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True,
                              default='img/avatar.jpg')

    def __str__(self):
        return f'Profile of {self.user.username}'

    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
