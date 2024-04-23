# Generated by Django 4.2.10 on 2024-03-10 08:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Income",
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
                (
                    "profession",
                    models.CharField(
                        choices=[
                            ("doctor", "Doctor"),
                            ("engineer", "Engineer"),
                            ("teacher", "Teacher"),
                        ],
                        max_length=100,
                    ),
                ),
                ("source_1_name", models.CharField(blank=True, max_length=100)),
                (
                    "source_1_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("source_2_name", models.CharField(blank=True, max_length=100)),
                (
                    "source_2_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("source_3_name", models.CharField(blank=True, max_length=100)),
                (
                    "source_3_amount",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("date", models.DateField(verbose_name=datetime.datetime.today)),
                (
                    "category",
                    models.CharField(
                        choices=[("income", "Income"), ("expense", "Expense")],
                        default="income",
                        max_length=10,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Income",
                "verbose_name_plural": "Income",
            },
        ),
    ]