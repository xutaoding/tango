# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-24 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0002_auto_20160724_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, blank=True),
            preserve_default=False,
        ),
    ]