# Generated by Django 3.1.13 on 2021-11-11 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211111_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyCategories',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.ManyToManyField(to='users.Categorie')),
            ],
        ),
    ]
