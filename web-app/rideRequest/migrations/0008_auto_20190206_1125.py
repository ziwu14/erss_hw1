# Generated by Django 2.1.5 on 2019-02-06 16:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideRequest', '0007_requestride_join_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestride',
            name='join_list',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(max_length=246), default=list, null=True, size=4),
        ),
    ]
