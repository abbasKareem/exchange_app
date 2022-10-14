# Generated by Django 4.1.2 on 2022-10-09 21:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0004_transcation"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "hawala_number",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("Pending", "Pending"),
                            ("Success", "Success"),
                            ("Fail", "Fail"),
                        ],
                        default=("Pending", "Pending"),
                        max_length=50,
                    ),
                ),
                ("mac_in", models.CharField(max_length=100)),
                ("mac_out", models.CharField(max_length=100)),
                ("recvied_amount", models.FloatField()),
                (
                    "transcation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="exchange.transcation",
                    ),
                ),
            ],
        ),
    ]