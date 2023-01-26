from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=14)
    is_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    ID = models.CharField(max_length=12,unique=True)
    gender = models.CharField(max_length=10,choices=[('Male','Male'),('Female','Female'),('Other','Other')])
    blood_Group = models.CharField(max_length=3,choices=[('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),('O+','O+'),('O-','O-'),('AB+','AB+'),('AB-','AB-')])
    profile_img = models.ImageField(upload_to='pics')
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True,blank=True)
    passcode = models.CharField(max_length=4)
    expiry = models.DateTimeField(null=True,blank=True)
    


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Prescriptions(models.Model):
    ID = models.CharField(max_length=12)
    date = models.CharField(max_length=15)
    prescription_img = models.ImageField(upload_to='prescriptions_pics')

