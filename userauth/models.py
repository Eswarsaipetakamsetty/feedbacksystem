from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)
    manager_id = models.ForeignKey('self', null = True, on_delete=models.SET_NULL, related_name='team')

    USERNAME_FIELD ='email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username