# Generated by Django 5.0.6 on 2024-07-05 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0016_vehicleslist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleslist',
            name='age',
        ),
        migrations.AlterField(
            model_name='vehicleslist',
            name='cost_of_purchase',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='vehicleslist',
            name='insurance_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='vehicleslist',
            name='maintenance_cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='vehicleslist',
            name='resale_value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]