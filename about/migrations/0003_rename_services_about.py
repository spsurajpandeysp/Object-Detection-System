# Generated by Django 4.2.7 on 2023-11-30 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_services_created_at_services_updated_at'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Services',
            new_name='About',
        ),
    ]
