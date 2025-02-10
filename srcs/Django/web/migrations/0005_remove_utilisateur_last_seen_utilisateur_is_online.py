# Generated by Django 5.1.4 on 2025-02-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_alter_friendrequest_options_utilisateur_last_seen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='last_seen',
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='is_online',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
