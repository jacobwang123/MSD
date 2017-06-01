# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-03 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='album',
        ),
        migrations.AddField(
            model_name='track',
            name='artist',
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
