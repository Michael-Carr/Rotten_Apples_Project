# Generated by Django 3.2 on 2021-06-10 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rotten_apples_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vgame',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
