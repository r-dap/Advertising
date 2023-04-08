from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django import forms
from django.core.files.storage import FileSystemStorage
import os
import subprocess
import json
import signal

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
    # print(type(files_path),':',files_path)
    context = {
        'media_files':files_path
    }
    return render(request, 'play.html', context)

# Choose file that need to be opened in play page
def show_file(request, file_path):
    try:
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
        subprocess.run(['xdg-open', file_full_path]) # Linux/Mac
        # subprocess.run(['open', file_full_path]) # MacOS
        # subprocess.run(['start', '', file_full_path], shell=True) # Windows

        # after open the file, automatically return to previous page
        return HttpResponse('<script>window.history.back();</script>')

    except:
        return render(request, 'play.html', {'message':'File not found！'})

# 當urls.py中的path('delete/',views.delete,name='delete file')被觸發時，會執行此函式
# 此函數會接到一個從play.html傳來的request，並且會取得request中的file_path
# 然後把file_path傳給delete_file函式，並且把delete_file函式的回傳值傳給play.html
def delete(request):
    file_path = request.POST.get('file')
    print(file_path)
    response = delete_file(file_path)
    print(response)
    return render(request, 'delete.html', {'message':response,'file':file_path})

# Delete file
def delete_file(file_path):
    
    file_full_path = '/home/you/桌面/advertising/' + file_path
    print(file_full_path, type(file_full_path))
    os.remove(file_full_path)
    return '檔案刪除成功！'

def control_player(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
      
        action = data.get('action')

        if action == 'Pause':
            subprocess.run(['xdotool','key','space'])
        
        # 關閉還不能用
        elif action == 'Stop':
            process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
            out, err = process.communicate()
            for line in out.splitlines():
                if b'vlc' in line:
                    pid = int(line.split(None, 1)[0])
                    print("Killing process: ", pid, "")
                    os.kill(pid, signal.SIGKILL)
    return JsonResponse({'message':'success'})