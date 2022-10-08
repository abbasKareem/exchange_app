from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone, username, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        # other_fields.setdefault('is_active', True)

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, phone, username, password, **other_fields)

    def create_user(self, email, phone, username, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        if not phone:
            raise ValueError('You must provide phone number')

        user = self.model(email=email, phone=phone,
                          username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=100, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'username',  'first_name', 'last_name']

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
