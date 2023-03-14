from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.
def index(request):
    return render(request,'index.html')

def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        return render(request, 'upload_file.html', {'message':'檔案上傳成功！'})
    return render(request, 'upload_file.html')
