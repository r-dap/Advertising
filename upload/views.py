from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django import forms
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

def index(request):
    return render(request,'index.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('file')
            if len(files) < 1:
                return render(request, 'upload_file.html', {'message':'請至少選擇一個檔案！'})
            fs = FileSystemStorage()
            for file in files:
                fs.save(file.name, file)
            return render(request, 'upload_file.html', {'message':'檔案上傳成功！'})
    else:
        form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form})

def play(request):
    # 取得目標目錄的路徑
    directory = os.path.join(settings.MEDIA_ROOT)
    # 讀取目錄中的所有文件
    files = os.listdir(directory)
    # 傳遞文件列表到模板中
    files_path = [os.path.join(settings.MEDIA_URL,file) for file in files]
    context = {
        'media_files':files_path
    }
    return render(request, 'play.html', context)

def show_file(request, file_path):
    try:
        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'rb') as f:
            file_data = f.read()
        return HttpResponse(file_data, content_type='application/octet-stream')
    except:
        return HttpResponse("File not found")
