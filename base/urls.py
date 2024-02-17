from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('download-all/', views.download_all, name='download_all'),
    path('photo/<str:pk>/', views.individual_photo, name='photo'),
    path('galleries/', views.galleries, name='galleries'),
    path('create-gallery', views.create_gallery, name='create_gallery'),
    path('galleries/<str:pk>/', views.individual_gallery, name='individual_galley'),
    path('upload/<str:pk>/', views.photo_upolad_to_gallery, name='photo_upolad_to_gallery'),
]
