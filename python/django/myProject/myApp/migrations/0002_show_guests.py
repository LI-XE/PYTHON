# Generated by Django 4.2.1 on 2023-05-28 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='guests',
            field=models.ManyToManyField(related_name='shows', to='myApp.user'),
        ),
    ]
