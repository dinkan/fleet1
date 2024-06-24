from rest_framework import serializers  
from .models import vehicle, Organization
  
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