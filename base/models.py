from django.db import models
from django.contrib.auth.models import User

from .utils import compress_image


class Gallery(models.Model):
    title = models.CharField(max_length=30, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - id:{self.id}'


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True)


    class Meta:
        ordering = ['-uploaded_at']


    def __str__(self):
        return str(self.image)

    
    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)

        super().save(*args, **kwargs)


class GalleryAccess(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('gallery', 'user')