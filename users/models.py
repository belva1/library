from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    # default=False - позволяет при создании объекта устанавливать дефолтное значение для поля
    is_librarian = models.BooleanField(default=False)
