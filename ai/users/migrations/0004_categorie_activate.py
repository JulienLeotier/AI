# Generated by Django 3.1.13 on 2021-11-11 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_categorie_musique'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='activate',
            field=models.BooleanField(default=True, verbose_name='activate'),
        ),
    ]
