# Generated by Django 5.0.6 on 2024-07-05 12:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0015_depot'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehiclesList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_purchase', models.DateField()),
                ('cost_of_purchase', models.FloatField()),
                ('vin_number', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=255)),
                ('maintenance_cost', models.FloatField()),
                ('insurance_cost', models.FloatField()),
                ('resale_value', models.FloatField()),
                ('depot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='depot_vehicles', to='vehicles.depot')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles_list', to='vehicles.organization')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_list', to='vehicles.vehicle')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warehouse_vehicles', to='vehicles.parkinglot')),
            ],
        ),
    ]
