# Generated by Django 5.1.4 on 2025-01-28 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='online_status',
            field=models.BooleanField(default=False),
        ),
    ]
