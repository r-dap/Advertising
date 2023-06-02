from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'), 
    path('upload/', views.upload_file,name='upload file'), # 上傳文件頁面
    path('upload/play/',views.play), # `播放頁面
    path('delete/',views.delete,name='delete'), # `刪除按鈕
    path('media/<path:file_path>/',views.show_file,name='show file'), # 播放影片
    path('navigation/',views.navigation,name='navigation'),
    path('getduration/',views.get_duration,name='get duration'), # 取得影片長度
    path('controlplayer/',views.control_player,name='control player'), # 控制播放器，暫停 撥放 停止
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # 靜態文件路徑，用來讀static資料夾的檔案
