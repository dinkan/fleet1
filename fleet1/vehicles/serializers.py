from rest_framework import serializers  
from .models import vehicle  
  
class vehicleSerializer(serializers.ModelSerializer):  
    name = serializers.CharField(max_length=200, required=True)  
    rollnumber = serializers.IntegerField()  
    class Meta:  
        model = vehicle
        fields = ('__all__')  
  
    def create(self, validated_data):  
        return vehicle.objects.create(**validated_data)  
  
    def update(self, instance, validated_data):  
        instance.name = validated_data.get('name', instance.name)  
        instance.rollnumber = validated_data.get('rollnumber', instance.rollnumber)  
        instance.save()  
        return instance  
