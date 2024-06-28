from django.contrib import admin
from .models import vehicle, Organization, ParkingLot, WarehouseInventory, Transaction
# Register your models here.

admin.site.register(vehicle)
admin.site.register(Organization)
admin.site.register(ParkingLot)
admin.site.register(WarehouseInventory)
admin.site.register(Transaction)