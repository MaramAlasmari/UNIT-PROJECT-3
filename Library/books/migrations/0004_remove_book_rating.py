# Generated by Django 5.0 on 2023-12-10 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='rating',
        ),
    ]