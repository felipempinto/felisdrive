from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.text import slugify
import os

class APIToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def get_created_at(self):
        return naturaltime(self.created_at)
    
    def get_expires_at(self):
        return naturaltime(self.expires_at)

class Folder(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, editable=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
image_formats = [
    ".png",
    ".jpg",
    ".jpeg"
]

class Data(models.Model):
    file = models.FileField()
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    access = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name
    
    def get_created_at(self):
        return naturaltime(self.created_at)
    
    def get_file(self):
        return os.path.basename(self.file.name)
    
    def get_format(self):
        return os.path.splitext(self.file.name)[-1]
    
    def is_image(self):
        if os.path.splitext(self.file.name)[-1] in image_formats:
            return True
        return False