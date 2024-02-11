from django.urls import path

from . import views

app_name = 'base'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('download-all/', views.download_all, name='download_all'),
    path('photo/<str:pk>/', views.individual_photo, name='photo'),
]
