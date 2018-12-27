# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-30 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metDNACore', '0010_auto_20171227_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=128, unique=True, verbose_name='email address'),
        ),
    ]
