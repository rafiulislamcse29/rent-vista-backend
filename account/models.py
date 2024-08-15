
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from rest_framework.authtoken.models import Token


class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'user'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES,default='user')



class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE )
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.account_no}"
  
    class Meta:
        verbose_name_plural = "UserBankAccount"
