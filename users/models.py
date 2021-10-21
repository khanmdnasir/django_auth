from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(AbstractUser):
    profile_image=models.ImageField(max_length=255,upload_to='profile_images',blank=True,null=True)
    nid_image=models.ImageField(max_length=255,upload_to='nid_images',blank=True,null=True)
    phone_number = PhoneNumberField(unique=True)
    is_teacher=models.BooleanField(default=False)
    is_email_verified=models.BooleanField(default=False)
    is_phone_verified=models.BooleanField(default=False)
    otp=models.CharField(max_length=6)
    
