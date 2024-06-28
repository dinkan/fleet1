from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import WarehouseInventory, Transaction

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
