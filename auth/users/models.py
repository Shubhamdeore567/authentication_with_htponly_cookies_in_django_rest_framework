from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.CharField(max_length=200, unique=True)
    phone = models.IntegerField(null=True)
    password = models.CharField(max_length=200)
    username = None
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=500,null=True)
    email_token = models.CharField(max_length=200,null=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    age = models.IntegerField(null=True)
    is_agreeed_terms = models.BooleanField(default=False)
    is_agreed_platform_rules = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    is_power_seller = models.BooleanField(default=False)
    is_allow_advertising = models.BooleanField(default=False)
    profile_picture = models.TextField(null=True)
    id_picture = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
