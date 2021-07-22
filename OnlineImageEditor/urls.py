from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mainApp.url_mainApp')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
