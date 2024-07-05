from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class vehicle(models.Model):
  vehnumber = models.IntegerField()
  name = models.CharField(max_length=255)
  vehicle_id = models.CharField(max_length=50, null=True, blank=True)
  vehicle = models.CharField(max_length=255, null=True, blank=True)
  size = models.CharField(max_length=50, null=True, blank=True)
  year = models.IntegerField(null=True, blank=True)
  cost = models.FloatField(null=True, blank=True)
  yearly_range_km = models.IntegerField(null=True, blank=True)
  distance = models.CharField(max_length=50, null=True, blank=True)
  
  def __str__(self):
      return f"{self.name} ({self.vehicle_id})" if self.vehicle_id else self.name

class Organization(models.Model):
    org_name = models.CharField(max_length=255)
    org_contact_email = models.EmailField()

    def __str__(self):
        return self.org_name

class ParkingLot(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='parkinglots')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.organization.org_name} - {self.name}"
    
class WarehouseInventory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventory')
    warehouse = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='warehouse_inventory')
    vehicle = models.ForeignKey(vehicle, on_delete=models.CASCADE, related_name='vehicle_inventory')
    date_of_purchase = models.DateField()
    cost_of_purchase = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return f"{self.organization.org_name} - {self.warehouse.name} - {self.vehicle.name} ({self.count})"
    
class Transaction(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    details = models.TextField()
    expense = models.FloatField()
    income = models.FloatField(default=0.0)
    reference_id = models.ForeignKey(WarehouseInventory, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        if self.reference_id:
            return f"{self.organization.org_name} - {self.reference_id.warehouse.name} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
        else:
            return f"{self.organization.org_name} - {self.date.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Fuel(models.Model):
    fuel_type = models.CharField(max_length=50)
    year = models.IntegerField()
    emissions_per_unit_fuel = models.FloatField()
    cost_per_unit_fuel = models.FloatField()
    cost_uncertainty = models.IntegerField()

    def __str__(self):
        return f"{self.fuel_type} ({self.year})"

class VehicleFuel(models.Model):
    vehicle_id = models.ForeignKey(vehicle, on_delete=models.CASCADE, related_name='vehicle_ids', null=True, blank=True)
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, related_name='fuels')
    consumption_per_km = models.FloatField()

    def __str__(self):
        return f"{self.vehicle_id.vehicle_id} - {self.fuel.fuel_type} ({self.fuel.year})"
    
class EmissionTarget(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    carbon_emission = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.organization.org_name} - {self.year}'
    
class FleetDemand(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    year = models.IntegerField()
    size = models.CharField(max_length=255)
    distance = models.CharField(max_length=255)
    demand = models.IntegerField()

    def __str__(self):
        return f"{self.organization.org_name} - {self.year} - {self.demand} km"
    
class DistanceTravelled(models.Model):
    vehicle_id = models.ForeignKey(WarehouseInventory, on_delete=models.CASCADE)
    date = models.DateField()
    distance_travelled = models.FloatField()
    fuel_used = models.ForeignKey(VehicleFuel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vehicle_id.vehicle.vehicle_id} - {self.distance_travelled} km on {self.date}"

class CostProfile(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    end_of_year = models.IntegerField()
    resale_value_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    insurance_cost_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    maintenance_cost_percent = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.organization.org_name} - End of Year {self.end_of_year} (id {self.id})"

class Depot(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='depots')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    parking_capacity = models.IntegerField()
    charging_points = models.IntegerField()

    def __str__(self):
        return f"{self.organization.org_name} - {self.name} (Capacity: {self.parking_capacity}, Charging Points: {self.charging_points})"
    
class VehiclesList(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='vehicles_list')
    depot = models.ForeignKey(Depot, on_delete=models.CASCADE, related_name='depot_vehicles')
    warehouse = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='warehouse_vehicles')
    vehicle = models.ForeignKey(vehicle, on_delete=models.CASCADE, related_name='vehicle_list')
    date_of_purchase = models.DateField()
    cost_of_purchase = models.FloatField()
    vin_number = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=255)
    maintenance_cost = models.FloatField()
    insurance_cost = models.FloatField()
    resale_value = models.FloatField()

    def __str__(self):
        return f"{self.organization.org_name} - {self.depot.name} - {self.vehicle.name} (VIN: {self.vin_number})"