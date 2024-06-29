# Generated by Django 5.0.6 on 2024-06-28 15:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0008_fuel_vehiclefuel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiclefuel',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='vehiclefuel',
            name='vehicle_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_ids', to='vehicles.vehicle'),
        ),
        migrations.AlterField(
            model_name='vehiclefuel',
            name='fuel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fuels', to='vehicles.fuel'),
        ),
    ]
