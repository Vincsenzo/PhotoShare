from django.core.files import File
from PIL import Image, ImageOps
from io import BytesIO


def compress_image(image):
    img = Image.open(image)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((1700, 1700))

    img_format = image.name.split('.')[-1].upper()

    io = BytesIO()
    img.save(io, img_format, qulity=85)
    compressed_img = File(io, name=image.name)
    return compressed_img
