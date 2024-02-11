from django.db import models

from .utils import compress_image


class Photo(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-uploaded']


    def __str__(self):
        return str(self.image)

    
    def save(self, *args, **kwargs):
        self.image = compress_image(self.image)

        super().save(*args, **kwargs)