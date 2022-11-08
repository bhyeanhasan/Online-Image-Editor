import os
import uuid
import numpy as np
from PIL import Image
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import SelectedImage


def home(request):
    return render(request, 'index.html')


def getImage(request):
    if 'imageToEdit' in request.FILES:
        image_file = request.FILES['imageToEdit']
        setPic = SelectedImage.objects.get(user=request.user)

        setPic.image = image_file
        setPic.save()

        image = Image.open(setPic.image)
        editing = np.array(image)
        if len(editing[0][0]) > 3:
            image = image.convert('RGB')
            editing = np.array(image)
        image.close()

        management(editing, request.user)

    return redirect('canvas')


def management(ary, user):
    img_new = Image.fromarray(ary)
    # name = str(uuid.uuid4()) + '.png'
    name = 'edit.jpeg'
    img_new.save('media/edit/' + name)
    editImageName = 'edit/' + name
    setPic = SelectedImage.objects.get(user=user)
    setPic.editImage = editImageName
    setPic.save()


def editImage_pixel(user):
    editing = np.array([1, 2, 3, 4])
    user = SelectedImage.objects.get(user=user)
    image = Image.open(user.editImage)
    editing = np.array(image)
    if len(editing[0][0]) > 3:
        image = image.convert('RGB')
        editing = np.array(image)
    image.close()
    return editing


def undo_all(request):
    setPic = SelectedImage.objects.get(user=request.user)
    setPic.editImage = setPic.image
    setPic.save()
    return redirect('canvas')


def crop(request):
    editing = editImage_pixel(request.user)
    new_editing = editing[50:, 50:, 0:]
    management(new_editing, request.user)
    return redirect('canvas')


def toGray(request):
    editing = editImage_pixel(request.user)

    for i in range(len(editing)):
        for j in range(len(editing[i])):
            valu = (editing[i][j][0] + editing[i][j][1] + editing[i][j][2]) / 3
            editing[i][j][0] = valu
            editing[i][j][1] = valu
            editing[i][j][2] = valu

    management(editing, request.user)
    return redirect('canvas')


def brightness(request, brightness_type):
    editing = editImage_pixel(request.user)
    bright = 50

    if brightness_type == "high":
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
    else:
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
    editing = editImage_pixel(request.user)
    for i in range(len(editing)):
        for j in range(len(editing[i])):
            r, g, b = editing[i][j]

            editing[i][j][0] = 255 - r
            editing[i][j][1] = 255 - g
            editing[i][j][2] = 255 - b

    management(editing, request.user)
    return redirect('canvas')


def pixel_value(r, g, b):
    if (r > 254):
        r = 254
    elif (r < 0):
        r = 0
    if (g > 254):
        g = 254
    elif (g < 0):
        g = 0
    if (b > 254):
        b = 254
    elif (b < 0):
        b = 0


    return [r, g, b]


############################################################################
############################################################################
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
