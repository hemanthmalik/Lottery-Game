from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=10)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AddedMoney(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reference_number = models.CharField(max_length=40)
    date_added = models.DateTimeField(default=timezone.now)