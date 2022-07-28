from webbrowser import get
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import get_hasher

# Create your models here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=255)
    email= models.CharField(max_length=255, unique=True)
    password= models.CharField(max_length=255)
    username= models.CharField(max_length=255, unique=True)

    REQUIRED_FIELDS= []

    def check_password(self, raw_password):
        hasher_type = "default"
        hasher = get_hasher(hasher_type)
        return  hasher.verify(raw_password, self.password)
    