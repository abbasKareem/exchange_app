# Generated by Django 4.1.2 on 2022-10-09 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("exchange", "0003_type_is_public"),
    ]

    operations = [
        migrations.CreateModel(
            name="Transcation",
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
                ("amount", models.FloatField()),
                (
                    "tran_from",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exchange.type"
                    ),
                ),
                (
                    "tran_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="transcation_to",
                        to="exchange.type",
                    ),
                ),
            ],
        ),
    ]
