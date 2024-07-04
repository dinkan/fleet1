from django.contrib import admin
from .models import vehicle, Organization, ParkingLot, WarehouseInventory, Transaction, Fuel, VehicleFuel, EmissionTarget, FleetDemand, DistanceTravelled, CostProfile
# Register your models here.

admin.site.register(vehicle)
admin.site.register(Organization)
admin.site.register(ParkingLot)
admin.site.register(WarehouseInventory)
admin.site.register(Transaction)
admin.site.register(Fuel)
admin.site.register(VehicleFuel)
admin.site.register(EmissionTarget)
admin.site.register(FleetDemand)
admin.site.register(DistanceTravelled)
admin.site.register(CostProfile)