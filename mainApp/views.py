from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request,'index.html')
def getImage(request):
    if 'imageToEdit' in request.FILES:
        image = request.FILES['profile_pic']
    return render(request, 'canvas.html',{'imageToedit':image})
