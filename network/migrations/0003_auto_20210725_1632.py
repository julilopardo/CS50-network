# Generated by Django 3.1.7 on 2021-07-25 19:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20210719_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='follow',
        ),
        migrations.RemoveField(
            model_name='like',
            name='liked',
        ),
    ]
