# Generated by Django 3.2.4 on 2021-06-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccines', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]