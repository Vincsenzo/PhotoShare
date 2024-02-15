import os
import zipfile
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf import settings

from .models import Photo, Gallery
from .forms import ImageUploadForm
from .storage import StorageSizeLimitExceeded


def index(request):
    images = Photo.objects.all()
    context = {'images': images}
    return render(request, 'base/index.html', context)


def upload_photo(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                for image in request.FILES.getlist('images'):
                    Photo.objects.create(image=image)
            except StorageSizeLimitExceeded as e:
                return HttpResponseBadRequest(str(e))
            return redirect('base:index')
        
    else:
        form = ImageUploadForm()

    context = {'form':form}
    return render(request, 'base/upload.html', context)


def download_all(request):
    images = Photo.objects.all()
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


# You can't access this view in any HTML template (this could change in the furure)
def individual_photo(request, pk):
    image = Photo.objects.get(id=pk)
    context = {'image': image}
    return render(request, 'base/photo.html', context)
