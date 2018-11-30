# Generated by Django 2.0.9 on 2018-11-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0047_add_markdown'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationbase',
            name='slack_channel',
            field=models.TextField(blank=True, help_text='The slack #channel for notifications. Default channel is #webapp-test'),
        ),
        migrations.AddField(
            model_name='labbase',
            name='slack_channel',
            field=models.TextField(blank=True, help_text='The slack #channel for notifications. Default channel is #webapp-test'),
        ),
    ]
