import os
import zipfile
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings

from .models import Photo, Gallery
from .forms import ImageUploadForm, GalleyForm
from .storage import StorageSizeLimitExceeded


def index(request):
    return redirect('base:galleries')


def download_all(request, pk):
    images = Photo.objects.filter(gallery=pk)
    zip_filename = 'images.zip'
    zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image in images:
            image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
            zipf.write(image_path, os.path.basename(image_path))

    zip_file = open(zip_filepath, 'rb')
    response = HttpResponse(zip_file, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return response


def galleries(request):
    galleries = Gallery.objects.all()
    context = {'galleries': galleries}
    return render(request, 'base/galleries.html', context)


def create_gallery(request):
    if request.method == 'POST':
        form = GalleyForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('base:galleries')
    
    else:
        form = GalleyForm()
    
    context = {'form': form}
    return render(request, 'base/create_gallery.html', context)


def individual_gallery(request, pk):
    images = Photo.objects.filter(gallery=pk)
    context = {'images': images, 'gallery_id': pk}
    return render(request, 'base/individual_gallery.html', context)


def upolad_to_gallery(request, pk):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        user = request.user
        if form.is_valid():
            gallery = Gallery.objects.get(id=pk)
            for image in request.FILES.getlist('images'):
                Photo.objects.create(image=image, uploaded_by=user, gallery=gallery)
        return redirect('base:individual_galley', pk=pk)

    else:
        form = ImageUploadForm()

    context = {'form':form}
    return render(request, 'base/upload.html', context)


def delete_photo(request, pk1, pk2):
    image = Photo.objects.get(id=pk2)
    image_file = image.image.path
    os.remove(image_file)
    image.delete()
    return redirect('base:individual_galley', pk=pk1)


# UNUSED CODE:

# def upload_photo(request):
#     if request.method == "POST":
#         form = ImageUploadForm(request.POST, request.FILES)
#         user = request.user
#         if form.is_valid():
#             gallery = form.cleaned_data['gallery']
#             try:
#                 for image in request.FILES.getlist('images'):
#                     Photo.objects.create(image=image, uploaded_by=user, gallery=gallery)
#             except StorageSizeLimitExceeded as e:
#                 return HttpResponseBadRequest(str(e))
#             return redirect('base:index')
        
#     else:
#         form = ImageUploadForm()

#     context = {'form':form}
#     return render(request, 'base/upload.html', context)


# You can't access this view in any HTML template (this could change in the furure)
# def individual_photo(request, pk):
#     image = Photo.objects.get(id=pk)
#     context = {'image': image}
#     return render(request, 'base/photo.html', context)