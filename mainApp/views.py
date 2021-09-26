import os
import uuid
import numpy as np
from PIL import Image
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SelectedImage

editing = np.array([1, 2, 3, 4, 5])


def home(request):
    return render(request, 'index.html')

def getImage(request):
    global editing
    if 'imageToEdit' in request.FILES:
        image_file = request.FILES['imageToEdit']
        setPic = SelectedImage.objects.get(user=request.user)
        setPic.image = image_file
        setPic.editImage = image_file
        setPic.save()

        image = Image.open(setPic.image)
        editing = np.array(image)
        if (len(editing[0][0]) > 3):
            image = image.convert('RGB')
            editing = np.array(image)
        image.close()
        print(editing)

    return redirect('canvas')


def management(ary, user):
    img_new = Image.fromarray(ary)
    # name = str(uuid.uuid4()) + '.png'
    name = 'edit.png'
    img_new.save('static_media/edit/' + name)
    editImageName = 'edit/' + name
    setPic = SelectedImage.objects.get(user=user)
    setPic.editImage = editImageName
    setPic.save()


def toGray(request):
    for i in range(len(editing)):
        for j in range(len(editing[i])):
            valu = (editing[i][j][0] + editing[i][j][1] + editing[i][j][2]) / 3
            editing[i][j][0] = valu
            editing[i][j][1] = valu
            editing[i][j][2] = valu

    management(editing, request.user)
    return redirect('canvas')


def brightness_plus(request):
    bright = 50
    for i in range(len(editing)):
        for j in range(len(editing[i])):
            r, g, b = editing[i][j]
            r += bright
            g += bright
            b += bright
            r, g, b = pixel_value(r, g, b)

            editing[i][j][0] = r
            editing[i][j][1] = g
            editing[i][j][2] = b
    management(editing, request.user)
    return redirect('canvas')


def brightness_minus(request):
    bright = 50
    for i in range(len(editing)):
        for j in range(len(editing[i])):
            r, g, b = editing[i][j]
            r -= bright
            g -= bright
            b -= bright
            r, g, b = pixel_value(r, g, b)

            editing[i][j][0] = r
            editing[i][j][1] = g
            editing[i][j][2] = b
    management(editing, request.user)
    return redirect('canvas')


def negative(request):
    bright = 0
    for i in range(len(editing)):
        for j in range(len(editing[i])):
            r, g, b = editing[i][j]

    management(editing, request.user)
    return redirect('canvas')


def pixel_value(r, g, b):
    if (r > 254):
        r = 254
    if (g > 254):
        g = 254
    if (b > 254):
        b = 254

    return [r, g, b]


############################################################################

def canvas(request):
    obg = SelectedImage.objects.get(user=request.user)
    return render(request, 'canvas.html', {'obg': obg})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return redirect('login')
    else:
        return redirect('login')
