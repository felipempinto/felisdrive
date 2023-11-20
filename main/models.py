from django.db import models
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime
import jwt
import datetime
from django.utils import timezone

class APIToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def get_created_at(self):
        return naturaltime(self.created_at)
    
    def get_expires_at(self):
        return naturaltime(self.expires_at)
    

class Data(models.Model):
    file = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Project()