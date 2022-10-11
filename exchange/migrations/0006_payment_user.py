# Generated by Django 4.1.2 on 2022-10-09 21:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0005_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
