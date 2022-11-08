import cv2
from PIL.Image import Image
from django.shortcuts import render, redirect
from mainApp.models import SelectedImage


def home(request):
    return render(request, 'index.html')


def getImage(request):
    if 'imageToEdit' in request.FILES:
        image_file = request.FILES['imageToEdit']
        try:
            setPic = SelectedImage.objects.get(user=request.user)
            setPic.image = image_file
            setPic.editImage = image_file
            setPic.save()
        except:
            obj = SelectedImage()
            obj.user = request.user
            obj.editImage = image_file
            obj.image = image_file
            obj.save()

        return redirect('canvas')


def canvas(request):
    obg = SelectedImage.objects.get(user=request.user)
    return render(request, 'canvas.html', {'obg': obg})


def save(request):
    obj = SelectedImage.objects.get(user=request.user)
    img = obj.editImage
    print(img.url)
    photo = cv2.imread(img.url)
    imaj = cv2.resize(photo,(600,600))
    obj.editImage = imaj
    obj.save()
    return redirect('canvas')
