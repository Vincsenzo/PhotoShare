from django.contrib import admin
import os

from .models import Photo, Gallery, GalleryAccess


def delete_model(modeladmin, request, queryset):
    for obj in queryset:
        img_file = obj.image.path
        os.remove(img_file)
        obj.delete()

delete_model.short_description = "Delete image files"


class PhotoAdmin(admin.ModelAdmin):
    actions = [delete_model]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Gallery)
admin.site.register(GalleryAccess)