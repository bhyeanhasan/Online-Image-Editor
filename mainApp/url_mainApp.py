from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getImage/', views.getImage, name='getImage'),
    path('canvas/', views.canvas, name='canvas'),
    path('toGray/', views.toGray, name='toGray'),
    path('brightness_plus/', views.brightness_plus, name='brightness_plus'),
    path('brightness_minus/', views.brightness_minus, name='brightness_minus'),
]