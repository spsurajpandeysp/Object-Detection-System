# Generated by Django 4.2.7 on 2023-12-10 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('complainApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complainmodel',
            name='image',
            field=models.FileField(default=False, max_length=250, null=True, upload_to='complainImage/'),
        ),
    ]
