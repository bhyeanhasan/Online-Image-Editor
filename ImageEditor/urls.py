from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getImage/', views.getImage, name='getImage'),
    path('canvas/', views.canvas, name='canvas'),
    path('save/', views.save, name='save'),
]