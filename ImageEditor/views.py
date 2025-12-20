import cv2
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from datetime import datetime
import numpy as np
from ImageEditor.models import SelectedImage
from django.conf import settings


@login_required
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
    img = obg.editImage.name

    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    x, y, z = img.shape
    return render(request, 'canvas.html', {'obg': obg, 'x': x, 'y': y})


def gray(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save(str(datetime.now()) + ".png", content)
    return redirect('canvas')


def negative(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    img = 255 - img

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def add_bright(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

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
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

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


def GaussianBlur(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    img = cv2.GaussianBlur(img, (7, 7), 0)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def medianBlur(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    img = cv2.medianBlur(img, 5)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def meanfilter(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Apply mean filter (box filter) to the image
    filtered_img = cv2.blur(img, (5, 5))  # (5, 5) is the kernel size, which can be adjusted

    # Save the mean-filtered image
    ret, buf = cv2.imencode('.jpg', filtered_img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('mean_filtered_output.jpg', content)

    return redirect('canvas')


def midpoint_filter(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Define kernel size for filtering
    kernel_size = (5, 5)

    # Apply maximum filter
    max_img = cv2.dilate(img, np.ones(kernel_size, np.uint8))

    # Apply minimum filter
    min_img = cv2.erode(img, np.ones(kernel_size, np.uint8))

    # Midpoint filter: average of max and min images
    midpoint_img = ((max_img.astype(np.float32) + min_img.astype(np.float32)) / 2).astype(np.uint8)

    # Save the midpoint-filtered image
    ret, buf = cv2.imencode('.jpg', midpoint_img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('midpoint_filtered_output.jpg', content)

    return redirect('canvas')


def crop_left(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if y > 20:
        img = img[:, 20:]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_right(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if y > 20:
        img = img[:, :y - 20]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_up(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if x > 20:
        img = img[20:, :]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def crop_down(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape
    if x > 20:
        img = img[:x - 20, :]

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)
    return redirect('canvas')


def undo(request):
    object = SelectedImage.objects.get(user=request.user)
    object.editImage = object.image
    object.save()
    return redirect('canvas')


def resize(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)
    x, y, z = img.shape

    if request.method == 'POST':
        height = int(request.POST['height'])
        width = int(request.POST['width'])

        if height > 0 and width > 0:
            img = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)

    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('output.jpg', content)

    return redirect('canvas')


def rotate_left(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if image is loaded properly
    if img is None:
        return redirect('canvas')  # handle error gracefully if the image is not found or fails to load

    # Rotate the image 90 degrees counter-clockwise
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)

    # Save the rotated image
    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('rotated_output.jpg', content)

    return redirect('canvas')


def rotate_right(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    # Check if the image is loaded properly
    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    # Rotate the image 90 degrees clockwise
    img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    # Save the rotated image
    ret, buf = cv2.imencode('.jpg', img)
    content = ContentFile(buf.tobytes())
    object.editImage.save('rotated_output_right.jpg', content)

    return redirect('canvas')


def detect_edge(request):
    object = SelectedImage.objects.get(user=request.user)
    img = object.editImage.name
    media_url = settings.MEDIA_ROOT
    media_url = media_url.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img)

    if img is None:
        return redirect('canvas')  # Handle error gracefully if the image is not found or fails to load

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray_img, threshold1=100, threshold2=200)

    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    ret, buf = cv2.imencode('.jpg', edges_color)
    content = ContentFile(buf.tobytes())
    object.editImage.save('edge_detected_output.jpg', content)

    return redirect('canvas')





def save(request):
    obj = SelectedImage.objects.get(user=request.user)
    img = obj.editImage
    photo = cv2.imread(img.url)
    imaj = cv2.resize(photo, (600, 600))
    obj.editImage = imaj
    obj.save()
    return redirect('canvas')

def custom_crop(request):
    if request.method == 'POST':
        try:
            object = SelectedImage.objects.get(user=request.user)
            img = object.editImage.name
            media_url = settings.MEDIA_ROOT
            media_url = media_url.replace('\\', "/")
            img = cv2.imread(media_url + '/' + img)

            x = int(float(request.POST.get('x')))
            y = int(float(request.POST.get('y')))
            width = int(float(request.POST.get('width')))
            height = int(float(request.POST.get('height')))

            # Ensure coordinates are valid
            if width > 0 and height > 0:
                # Crop format: img[y:y+h, x:x+w]
                cropped_img = img[y:y+height, x:x+width]
                
                ret, buf = cv2.imencode('.jpg', cropped_img)
                content = ContentFile(buf.tobytes())
                object.editImage.save('cropped_output.jpg', content)

        except Exception as e:
            print(f"Error cropping image: {e}")
            pass
            
    return redirect('canvas')

# --- New Feature Views ---

def flip_horizontal(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)
    
    if img is not None:
        img = cv2.flip(img, 1) # 1 for horizontal
        
        ret, buf = cv2.imencode('.jpg', img)
        content = ContentFile(buf.tobytes())
        object.editImage.save('flip_h_output.jpg', content)
        
    return redirect('canvas')

def flip_vertical(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)
    
    if img is not None:
        img = cv2.flip(img, 0) # 0 for vertical
        
        ret, buf = cv2.imencode('.jpg', img)
        content = ContentFile(buf.tobytes())
        object.editImage.save('flip_v_output.jpg', content)
        
    return redirect('canvas')

def contrast_boost(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        # Increase contrast: alpha > 1
        alpha = 1.25
        beta = 0
        img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        ret, buf = cv2.imencode('.jpg', img)
        content = ContentFile(buf.tobytes())
        object.editImage.save('contrast_boost.jpg', content)

    return redirect('canvas')

def contrast_reduce(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        # Decrease contrast: alpha < 1
        alpha = 0.8
        beta = 0
        img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        ret, buf = cv2.imencode('.jpg', img)
        content = ContentFile(buf.tobytes())
        object.editImage.save('contrast_reduce.jpg', content)

    return redirect('canvas')

def filter_sepia(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        img_sepia = np.array(img, dtype=np.float64) # converting to float to prevent loss
        img_sepia = cv2.transform(img_sepia, np.matrix([[0.272, 0.534, 0.131],
                                                        [0.349, 0.686, 0.168],
                                                        [0.393, 0.769, 0.189]])) # Multiplying image with special sepia matrix
        img_sepia[np.where(img_sepia > 255)] = 255 # Normalizing values greater than 255 to 255
        img_sepia = np.array(img_sepia, dtype=np.uint8)
        
        ret, buf = cv2.imencode('.jpg', img_sepia)
        content = ContentFile(buf.tobytes())
        object.editImage.save('sepia.jpg', content)

    return redirect('canvas')

def filter_sharpen(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        img = cv2.filter2D(img, -1, kernel)
        
        ret, buf = cv2.imencode('.jpg', img)
        content = ContentFile(buf.tobytes())
        object.editImage.save('sharpen.jpg', content)

    return redirect('canvas')

def filter_sketch(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        # Convert to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Invert
        inv = cv2.bitwise_not(gray)
        # Gaussian Blur
        blur = cv2.GaussianBlur(inv, (21, 21), 0)
        # Invert blur
        inv_blur = cv2.bitwise_not(blur)
        # Sketch
        sketch = cv2.divide(gray, inv_blur, scale=256.0)
        
        ret, buf = cv2.imencode('.jpg', sketch)
        content = ContentFile(buf.tobytes())
        object.editImage.save('sketch.jpg', content)

    return redirect('canvas')

def filter_vignette(request):
    object = SelectedImage.objects.get(user=request.user)
    img_name = object.editImage.name
    media_url = settings.MEDIA_ROOT.replace('\\', "/")
    img = cv2.imread(media_url + '/' + img_name)

    if img is not None:
        rows, cols = img.shape[:2]
        kernel_x = cv2.getGaussianKernel(cols, 200)
        kernel_y = cv2.getGaussianKernel(rows, 200)
        kernel = kernel_y * kernel_x.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        output = np.copy(img)
        
        for i in range(3):
            output[:,:,i] = output[:,:,i] * mask

        ret, buf = cv2.imencode('.jpg', output)
        content = ContentFile(buf.tobytes())
        object.editImage.save('vignette.jpg', content)

    return redirect('canvas')

def add_text(request):
    if request.method == 'POST':
        try:
            object = SelectedImage.objects.get(user=request.user)
            img_name = object.editImage.name
            media_url = settings.MEDIA_ROOT.replace('\\', "/")
            img = cv2.imread(media_url + '/' + img_name)

            text = request.POST.get('text', '')
            if img is not None and text:
                # Default settings for now
                font = cv2.FONT_HERSHEY_SIMPLEX
                # Calculate scale based on image size to make text visible
                scale = img.shape[0] / 1000.0 * 2 
                color = (255, 255, 255) # White
                thickness = max(1, int(scale * 2))
                
                # Center text for simplicity or fixed position
                text_size = cv2.getTextSize(text, font, scale, thickness)[0]
                text_x = int((img.shape[1] - text_size[0]) / 2)
                text_y = int((img.shape[0] + text_size[1]) / 2)

                cv2.putText(img, text, (text_x, text_y), font, scale, color, thickness, cv2.LINE_AA)
                
                ret, buf = cv2.imencode('.jpg', img)
                content = ContentFile(buf.tobytes())
                object.editImage.save('text_overlay.jpg', content)
        except Exception as e:
            print(f"Error adding text: {e}")
            pass
            
    return redirect('canvas')
