# Generated by Django 4.1.2 on 2022-10-10 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0008_payment_total"),
    ]

    operations = [
        migrations.RemoveField(model_name="customuser", name="username",),
    ]