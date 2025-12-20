from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getImage/', views.getImage, name='getImage'),
    path('canvas/', views.canvas, name='canvas'),
    path('save/', views.save, name='save'),
    path('undo/', views.undo, name='undo'),

    path('gray/', views.gray, name='gray'),
    path('rotate_left/', views.rotate_left, name='rotate_left'),
    path('rotate_right/', views.rotate_right, name='rotate_right'),
    path('detect_edge/', views.detect_edge, name='detect_edge'),
    path('meanfilter/', views.meanfilter, name='meanfilter'),
    path('midpoint_filter/', views.midpoint_filter, name='midpoint_filter'),
    path('negative/', views.negative, name='negative'),
    path('add_bright', views.add_bright, name='add_bright'),
    path('remove_bright', views.remove_bright, name='remove_bright'),
    path('GaussianBlur', views.GaussianBlur, name='GaussianBlur'),
    path('medianBlur', views.medianBlur, name='medianBlur'),
    path('crop_left', views.crop_left, name='crop_left'),
    path('crop_right', views.crop_right, name='crop_right'),
    path('crop_up', views.crop_up, name='crop_up'),
    path('crop_down', views.crop_down, name='crop_down'),
    path('canvas/resize', views.resize, name='resize'),
    path('custom_crop/', views.custom_crop, name='custom_crop'),
    
    # New Features
    path('flip_horizontal/', views.flip_horizontal, name='flip_horizontal'),
    path('flip_vertical/', views.flip_vertical, name='flip_vertical'),
    path('contrast_boost/', views.contrast_boost, name='contrast_boost'),
    path('contrast_reduce/', views.contrast_reduce, name='contrast_reduce'),
    path('filter_sepia/', views.filter_sepia, name='filter_sepia'),
    path('filter_sharpen/', views.filter_sharpen, name='filter_sharpen'),
    path('filter_sketch/', views.filter_sketch, name='filter_sketch'),
    path('filter_vignette/', views.filter_vignette, name='filter_vignette'),
    path('add_text/', views.add_text, name='add_text'),
]