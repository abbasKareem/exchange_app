import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid
from django.conf import settings

from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import send_notifiy


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, phone, password, **other_fields):

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

        return self.create_user(email, phone, password, **other_fields)

    def create_user(self, email, phone, password, **other_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)

        if not phone:
            raise ValueError('You must provide phone number')

        user = self.model(email=email, phone=phone,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=100, unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20, unique=True)
    # username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name } {self.last_name}"

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Type(models.Model):
    type_name = models.CharField(
        max_length=30, unique=True, blank=False, null=False)
    is_public = models.BooleanField(default=True)

    def __str__(self):
        return self.type_name


class Transcation(models.Model):
    tran_from = models.ForeignKey(Type, on_delete=models.CASCADE)
    tran_to = models.ForeignKey(
        Type, related_name='transcation_to', on_delete=models.CASCADE)
    amount = models.FloatField(blank=False, null=False)

    def __str__(self):
        return f"{self.tran_from.type_name} to {self.tran_to.type_name}"


STATUS = (
    ("Pending", "Pending"),
    ("Success", "Success"),
    ("Fail", "Fail")
)


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    create_at = models.DateTimeField(default=timezone.now)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    transcation = models.ForeignKey(Transcation, on_delete=models.CASCADE)
    hawala_number = models.CharField(
        max_length=20, unique=True, blank=True, null=True)
    status = models.CharField(
        max_length=50, choices=STATUS, default=STATUS[0])

    mac_in = models.CharField(max_length=100, blank=True, null=True)
    # mac_out store in me only
    mac_out = models.CharField(max_length=100, blank=False, null=False)

    recvied_amount = models.FloatField(blank=False, null=False)
    total = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.transcation.tran_from} to {self.transcation.tran_to}"

    def save(self, *args, **kwargs):
        # Check to see if no mac_out in the table if not mac_out then create one
        if not self.mac_out:
            mic_out_str = f"{self.user.pk}{self.transcation.tran_from}{self.recvied_amount}{self.transcation.tran_to}"
            result = hashlib.md5(mic_out_str.encode())
            result_final = result.hexdigest()
            self.mac_out = result_final

        if self.mac_in:
            # if there is mac_in we compare it with the mac_out and if they are not the same we change status to "Fail"
            if self.mac_in == self.mac_out:
                pass
            else:
                self.status = 'Fail'

        super(Payment, self).save(*args, **kwargs)


class Notification(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    body = models.CharField(max_length=200, blank=False, null=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class OneSignal(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_notify_id = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.user_notify_id


@receiver(post_save, sender=Payment)
def sent_notification_when_status_success(sender, instance, created, **kwargs):
    if created == False:
        if instance.status == 'Success':
            message = "Your Payment done👍, please go back to the app to see the payment"
            try:

                onesignal_ob = OneSignal.objects.get(user=instance.user)
                res = send_notifiy(onesignal_ob.user_notify_id, message)
                print(res)

                print("==========================================")
                message = f"Your exchange from {instance.transcation.tran_from} to {instance.transcation.tran_to} Accepted"
                print("==========================================")
                no_obj = Notification.objects.create(
                    user=instance.user, title="Accepted Payment!", body=message)
                no_obj.save()
            except OneSignal.DoesNotExist:
                print("not found")
        if instance.status == 'Fail':
            message = "Your Payment (Failed)🙁, please go back to the app to see the payment"
            try:
                onesignal_ob = OneSignal.objects.get(user=instance.user)
                res = send_notifiy(onesignal_ob.user_notify_id, message)
                print(res)
                print("==========================================")
                message = f"Your exchange from {instance.transcation.tran_from} to {instance.transcation.tran_to} Failed"
                print("==========================================")
                no_obj = Notification.objects.create(
                    user=instance.user, title="Failed Payment!", body=message)
                no_obj.save()
            except OneSignal.DoesNotExist:
                print("not found")

