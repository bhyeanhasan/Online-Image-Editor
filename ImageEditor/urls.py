from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getImage/', views.getImage, name='getImage'),
    path('canvas/', views.canvas, name='canvas'),
    path('save/', views.save, name='save'),
    path('undo/', views.undo, name='undo'),

    path('gray/', views.gray, name='gray'),
    path('negative/', views.negative, name='negative'),
    path('add_bright', views.add_bright, name='add_bright'),
    path('remove_bright', views.remove_bright, name='remove_bright'),
    path('GaussianBlur', views.GaussianBlur, name='GaussianBlur'),
    path('medianBlur', views.medianBlur, name='medianBlur'),
    path('crop_left', views.crop_left, name='crop_left'),
    path('crop_right', views.crop_right, name='crop_right'),
    path('crop_up', views.crop_up, name='crop_up'),
    path('crop_down', views.crop_down, name='crop_down'),
]