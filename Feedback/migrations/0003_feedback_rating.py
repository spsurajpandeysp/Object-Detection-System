# Generated by Django 4.2.7 on 2023-12-10 16:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Feedback', '0002_alter_feedback_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='rating',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
