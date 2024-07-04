from rest_framework import serializers  
from .models import vehicle, Organization, ParkingLot, WarehouseInventory, Fuel, VehicleFuel, EmissionTarget, FleetDemand, DistanceTravelled, Transaction, CostProfile

class vehicleSerializer(serializers.ModelSerializer):  
    name = serializers.CharField(max_length=200, required=True)  
    vehnumber = serializers.IntegerField()  
    class Meta:  
        model = vehicle
        fields = ('__all__')  
  
    def create(self, validated_data):  
        return vehicle.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
        instance.name = validated_data.get('name', instance.name)  
        instance.vehnumber = validated_data.get('vehnumber', instance.vehnumber)
        instance.vehicle_id = validated_data.get('vehicle_id', instance.vehicle_id)
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.size = validated_data.get('size', instance.size)
        instance.year = validated_data.get('year', instance.year)
        instance.cost = validated_data.get('cost', instance.cost)
        instance.yearly_range_km = validated_data.get('yearly_range_km', instance.yearly_range_km)
        instance.distance = validated_data.get('distance', instance.distance)  
        instance.save()  
        return instance  

class OrganizationSerializer(serializers.ModelSerializer):
    org_name = serializers.CharField(max_length=255, required=True)
    org_contact_email = serializers.EmailField()

    class Meta:
        model = Organization
        fields = ('__all__')

    def create(self, validated_data):
        return Organization.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.org_name = validated_data.get('org_name', instance.org_name)
        instance.org_contact_email = validated_data.get('org_contact_email', instance.org_contact_email)
        instance.save()
        return instance
    
class ParkingLotSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255, required=True)
    address = serializers.CharField(max_length=255, required=True)

    class Meta:
        model = ParkingLot
        fields = '__all__'

    def create(self, validated_data):
        return ParkingLot.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
    
class WarehouseInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseInventory
        fields = '__all__'

    def create(self, validated_data):
        return WarehouseInventory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)
        instance.vehicle = validated_data.get('vehicle', instance.vehicle)
        instance.date_of_purchase = validated_data.get('date_of_purchase', instance.date_of_purchase)
        instance.cost_of_purchase = validated_data.get('cost_of_purchase', instance.cost_of_purchase)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        return instance
    
class FuelSerializer(serializers.ModelSerializer):  
    fuel_type = serializers.CharField(max_length=50, required=True)  
    year = serializers.IntegerField()  
    
    class Meta:  
        model = Fuel
        fields = '__all__'  
  
    def create(self, validated_data):  
        return Fuel.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
        instance.fuel_type = validated_data.get('fuel_type', instance.fuel_type)  
        instance.year = validated_data.get('year', instance.year)
        instance.emissions_per_unit_fuel = validated_data.get('emissions_per_unit_fuel', instance.emissions_per_unit_fuel)
        instance.cost_per_unit_fuel = validated_data.get('cost_per_unit_fuel', instance.cost_per_unit_fuel)
        instance.cost_uncertainty = validated_data.get('cost_uncertainty', instance.cost_uncertainty)
        instance.save()  
        return instance  

class VehicleFuelSerializer(serializers.ModelSerializer):  
    
    class Meta:  
        model = VehicleFuel
        fields = '__all__'  
  
    def create(self, validated_data):  
        return VehicleFuel.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
        instance.vehicle_id = validated_data.get('vehicle_id', instance.vehicle_id)  
        instance.fuel = validated_data.get('fuel', instance.fuel)
        instance.consumption_per_km = validated_data.get('consumption_per_km', instance.consumption_per_km)
        instance.save()  
        return instance

class EmissionTargetSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = EmissionTarget
        fields = ('__all__')

    def create(self, validated_data):
        return EmissionTarget.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.year = validated_data.get('year', instance.year)
        instance.carbon_emission = validated_data.get('carbon_emission', instance.carbon_emission)
        instance.save()
        return instance
    
class FleetDemandSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = FleetDemand
        fields = ('__all__')

    def create(self, validated_data):
        return FleetDemand.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.year = validated_data.get('year', instance.year)
        instance.size = validated_data.get('size', instance.size)
        instance.distance = validated_data.get('distance', instance.distance)
        instance.demand = validated_data.get('demand', instance.demand)
        instance.save()
        return instance
    
class DistanceTravelledSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceTravelled
        fields = '__all__'

    def create(self, validated_data):
        return DistanceTravelled.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.vehicle_id = validated_data.get('vehicle_id', instance.vehicle_id)
        instance.date = validated_data.get('date', instance.date)
        instance.distance_travelled = validated_data.get('distance_travelled', instance.distance_travelled)
        instance.fuel_used = validated_data.get('fuel_used', instance.fuel_used)
        instance.save()
        return instance
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def create(self, validated_data):
        return Transaction.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.date = validated_data.get('date', instance.date)
        instance.details = validated_data.get('details', instance.details)
        instance.expense = validated_data.get('expense', instance.expense)
        instance.income = validated_data.get('income', instance.income)
        instance.reference_id = validated_data.get('reference_id', instance.reference_id)
        instance.save()
        return instance
    
class CostProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostProfile
        fields = '__all__'

    def create(self, validated_data):
        return CostProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get('organization', instance.organization)
        instance.end_of_year = validated_data.get('end_of_year', instance.end_of_year)
        instance.resale_value_percent = validated_data.get('resale_value_percent', instance.resale_value_percent)
        instance.insurance_cost_percent = validated_data.get('insurance_cost_percent', instance.insurance_cost_percent)
        instance.maintenance_cost_percent = validated_data.get('maintenance_cost_percent', instance.maintenance_cost_percent)
        instance.save()
        return instance