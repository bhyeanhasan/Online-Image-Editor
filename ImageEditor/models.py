from django.contrib.auth.models import User
from django.db import models

class SelectedImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='pictures', null=True, blank=True)
    editImage = models.ImageField(upload_to='edit', null=True, blank=True)
