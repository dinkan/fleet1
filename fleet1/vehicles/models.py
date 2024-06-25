from django.db import models

# Create your models here.


class vehicle(models.Model):
  vehnumber = models.IntegerField()
  name = models.CharField(max_length=255)
  
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