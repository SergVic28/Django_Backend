# Generated by Django 3.2 on 2021-04-24 04:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0010_delete_feed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='text',
            field=models.TextField(),
        ),
    ]
