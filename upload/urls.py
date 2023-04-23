from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('upload/', views.upload_file,name='upload file'),
    path('upload/play/',views.play),
    path('delete/',views.delete,name='delete'),
    path('media/<path:file_path>/',views.show_file,name='show file'),
    path('controlplayer/',views.control_player,name='control player')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
