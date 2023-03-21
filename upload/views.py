from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django import forms
from django.core.files.storage import FileSystemStorage
import os
import subprocess

# Class for verify if the file is selected in function of upload_file
class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

# Home page
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

# Play page
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

# Choose file that need to be opened in play page
def show_file(request, file_path):
    try:
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        # subprocess.run(['xdg-open', file_full_path]) # Linux/Mac
        subprocess.run(['open', file_full_path]) # MacOS
        # subprocess.run(['start', '', file_full_path], shell=True) # Windows
        return HttpResponse("File opened")
    except:
        return HttpResponse("File not found")
