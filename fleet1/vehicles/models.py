from django.db import models

# Create your models here.


class vehicle(models.Model):
  vehnumber = models.IntegerField()
  name = models.CharField(max_length=255)
