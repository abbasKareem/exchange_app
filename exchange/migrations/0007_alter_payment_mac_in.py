# Generated by Django 4.1.2 on 2022-10-10 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0006_payment_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="mac_in",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
