from django.db import models

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
      return self.name

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
        return self.name
    
class WarehouseInventory(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventory')
    warehouse = models.ForeignKey(ParkingLot, on_delete=models.CASCADE, related_name='warehouse_inventory')
    vehicle = models.ForeignKey(vehicle, on_delete=models.CASCADE, related_name='vehicle_inventory')
    date_of_purchase = models.DateField()
    cost_of_purchase = models.FloatField()
    count = models.IntegerField()

    def __str__(self):
        return f"{self.warehouse.name} - {self.vehicle.name}"