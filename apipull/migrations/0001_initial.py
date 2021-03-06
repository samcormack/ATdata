# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RTentry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('id_no', models.CharField(max_length=100)),
                ('trip_id', models.CharField(max_length=100)),
                ('route_id', models.CharField(max_length=100)),
                ('stop_seq', models.IntegerField()),
                ('stop_id', models.IntegerField()),
                ('stop_type', models.CharField(max_length=20)),
                ('vehicle_id', models.IntegerField()),
                ('delay', models.IntegerField()),
                ('time', models.DateTimeField()),
            ],
        ),
    ]
