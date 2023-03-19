from django.contrib import admin
from django.urls import path

from . import views
urlpatterns = [
    path('', views.index,name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('play/',views.play),
    path('media/<path:file_path>/',views.show_file,name='show file')
]