from django.db import models

class Message(models.Model):
    fromWhom = models.CharField(max_length=50)
    toWhom = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
