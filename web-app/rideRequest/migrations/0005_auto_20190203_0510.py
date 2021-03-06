# Generated by Django 2.1.5 on 2019-02-03 10:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rideRequest', '0004_auto_20190203_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestride',
            name='remmaining_seat',
            field=models.IntegerField(default=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AddField(
            model_name='requestride',
            name='status_share',
            field=models.BooleanField(default=False),
        ),
    ]
