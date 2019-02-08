# Generated by Django 2.1.5 on 2019-02-03 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('driverRegister', '0003_auto_20190201_2216'),
        ('rideRequest', '0002_auto_20190202_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestride',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='driverRegister.Driver'),
        ),
    ]