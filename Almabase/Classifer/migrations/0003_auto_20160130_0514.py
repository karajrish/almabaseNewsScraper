# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-30 05:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Classifer', '0002_auto_20160130_0514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywords',
            name='keywords',
            field=models.ManyToManyField(blank=True, null=True, to='Classifer.KeywordList'),
        ),
    ]