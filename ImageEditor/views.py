import cv2
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from mainApp.models import SelectedImage
from datetime import datetime
import numpy as np


def home(request):
    return render(request, 'index.html')


@login_required
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


@login_required
def canvas(request):
    obg = SelectedImage.objects.get(user=request.user)
    return render(request, 'canvas.html', {'obg': obg})


def gray(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.url
    img = cv2.imread('./' + img)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save(str(datetime.now()) + ".png", content)
    return redirect('canvas')


def negative(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.url
    img = cv2.imread('./' + img)

    img = 255 - img

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def add_bright(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.url
    img = cv2.imread('./' + img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, 20)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def remove_bright(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.url
    img = cv2.imread('./' + img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.subtract(v, 20)
    v[v > 255] = 255
    v[v < 0] = 0
    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def undo(request):
    object = SelectedImage.objects.get(user=request.user)
    object.editImage = object.image
    object.save()
    return redirect('canvas')


def save(request):
    obj = SelectedImage.objects.get(user=request.user)
    img = obj.editImage
    print(img.url)
    photo = cv2.imread(img.url)
    imaj = cv2.resize(photo, (600, 600))
    obj.editImage = imaj
    obj.save()
    return redirect('canvas')
