from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.upload_file,name='upload file'),
    path('play/',views.play),
    path('media/<path:file_path>/',views.show_file,name='show file')
]
