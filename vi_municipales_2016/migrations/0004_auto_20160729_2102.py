# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-07-29 21:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vi_municipales_2016', '0003_auto_20160729_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='posiblefacebookpage',
            name='verified',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='posiblefacebookpage',
            name='candidate',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posible_facebook_pages', to='elections.Candidate'),
        ),
    ]
