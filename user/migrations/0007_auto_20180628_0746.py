# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-06-28 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20180627_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(default='', max_length=255, unique=True, verbose_name='组名'),
            preserve_default=False,
        ),
    ]