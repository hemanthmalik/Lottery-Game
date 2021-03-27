from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=60)
    phone = models.CharField(max_length=10, unique=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    balance = models.IntegerField(default=0)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    ordering = ('phone')

    objects = CustomUserManager()

    def __str__(self):
        return self.phone


class AddedAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    reference_number = models.CharField(max_length=40, unique=True)
    date_added = models.DateTimeField(default=timezone.now)
    validated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.validated:
            self.user.balance += self.amount
            self.user.save()
        super(AddedAmount, self).save(*args, **kwargs)


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField()
    amount = models.IntegerField()

class Win(models.Model):
    date = models.DateField(unique=True)
    winners = models.CharField(max_length=50)