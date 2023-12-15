# Generated by Django 5.0 on 2023-12-15 18:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_remove_clinica_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="paciente",
            name="clinica",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app.clinica",
            ),
        ),
    ]
