from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import WarehouseInventory, Transaction, DistanceTravelled

@receiver(post_save, sender=WarehouseInventory)
def create_or_update_transaction(sender, instance, created, **kwargs):
    cost_of_purchase = float(instance.cost_of_purchase)
    count = int(instance.count)
    total_cost = cost_of_purchase * count
    if created:
        Transaction.objects.create(
            organization=instance.organization,
            date=timezone.now(),
            details='Vehicle Purchase',
            expense=total_cost,
            income=0.0,
            reference_id=instance
        )
    else:
        Transaction.objects.filter(reference_id=instance).update(
            expense=total_cost,
            date=timezone.now()
        )

@receiver(post_delete, sender=WarehouseInventory)
def delete_transaction(sender, instance, **kwargs):
    Transaction.objects.filter(reference_id=instance).delete()

@receiver(post_save, sender=DistanceTravelled)
def create_or_update_travel_transaction(sender, instance, created, **kwargs):
    warehouseinventory = instance.vehicle_id
    fuel_cost = instance.fuel_used.fuel.cost_per_unit_fuel
    distance = instance.distance_travelled
    expense = float(distance) * float(fuel_cost)

    organization = warehouseinventory.organization

    if created:
        Transaction.objects.create(
            organization=organization,
            date=timezone.now(),
            details='Travelling Cost',
            expense=expense,
            income=0.0,
            reference_id=None
        )
    else:
        Transaction.objects.filter(
            organization=organization,
            details='Travelling Cost',
            reference_id=None
        ).update(
            date=timezone.now(),
            expense=expense
        )

@receiver(post_delete, sender=DistanceTravelled)
def delete_travel_transaction(sender, instance, **kwargs):
    warehouseinventory = instance.vehicle_id
    fuel_cost = instance.fuel_used.fuel.cost_per_unit_fuel
    distance = instance.distance_travelled
    expense = float(distance) * float(fuel_cost)

    organization = warehouseinventory.organization

    Transaction.objects.filter(
        organization=organization,
        details='Travelling Cost',
        expense=expense,
        income=0.0,
        reference_id=None
    ).delete()