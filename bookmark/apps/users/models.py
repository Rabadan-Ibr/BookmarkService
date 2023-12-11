import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.users.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Mодель пользователей."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=255,
    )
    first_name = models.CharField(
        verbose_name='Name',
        max_length=150,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Last_name',
        max_length=150,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    class Meta:
        ordering = ['-pk']
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
