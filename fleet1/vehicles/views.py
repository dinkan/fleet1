from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404

# Create your views here.

from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Hello world!")

from django.template import loader

from .models import vehicle, Organization, ParkingLot, WarehouseInventory, Transaction

from django.db.models import Sum

from django.core.exceptions import ValidationError

def vehicles(request):
  vehiclelist = vehicle.objects.all().values()
  template = loader.get_template('vehicleslist.html')
  context = {
    'vehiclelist': vehiclelist,
  }
  return HttpResponse(template.render(context, request))


def details(request, id):
  mymember = vehicle.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'thisvehicle': mymember,
  }
  return HttpResponse(template.render(context, request))

def update(request, id):
  mymember = vehicle.objects.get(id=id)
  template = loader.get_template('update.html')
  context = {
    'thisvehicle': mymember,
  }
  return HttpResponse(template.render(context, request))

def updatesub(request, id):
  mymember = vehicle.objects.get(id=id)
  mymember.vehnumber=request.POST["vehnumber"]
  mymember.name=request.POST["name"]
  mymember.vehicle_id = request.POST.get("vehicle_id")
  mymember.vehicle = request.POST.get("vehicle")
  mymember.size = request.POST.get("size")
  mymember.year = request.POST.get("year")
  mymember.cost = request.POST.get("cost")
  mymember.yearly_range_km = request.POST.get("yearly_range_km")
  mymember.distance = request.POST.get("distance")
  mymember.save()
  #return HttpResponse("Record updated")
  response = redirect('/vehicles')
  return response  

def deletesub(request, id):
  mymember = vehicle.objects.get(id=id)
  #mymember.vehnumber=request.POST["vehnumber"]
  #mymember.name=request.POST["name"]
  mymember.delete()
  #return HttpResponse("Record updated")
  response = redirect('/vehicles')
  return response  


def create(request):
  #mymember = vehicle.objects.get(id=id)
  template = loader.get_template('create.html')
  context = {
   
  }
  return HttpResponse(template.render(context, request))


def createsub(request):
  vehnumber=request.POST["vehnumber"]
  name=request.POST["name"]
  vehicle_id = request.POST.get("vehicle_id")
  vehicle_type  = request.POST.get("vehicle")
  size = request.POST.get("size")
  year = request.POST.get("year")
  cost = request.POST.get("cost")
  yearly_range_km = request.POST.get("yearly_range_km")
  distance = request.POST.get("distance")
  mymember = vehicle(vehnumber=vehnumber,name=name,vehicle_id=vehicle_id,vehicle=vehicle_type,size=size,year=year,cost=cost,yearly_range_km=yearly_range_km,distance=distance)
  mymember.save()
  response = redirect('/vehicles')
  return response


def organization(request):
    organization_list = Organization.objects.all().values()
    template = loader.get_template('organizationlist.html')
    context = {
        'organization_list': organization_list,
    }
    return HttpResponse(template.render(context, request))

def org_details(request, id):
    organization = Organization.objects.get(id=id)
    template = loader.get_template('org_details.html')
    context = {
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def org_create(request):
    template = loader.get_template('org_create.html')
    context = {}
    return HttpResponse(template.render(context, request))

def org_createsub(request):
    org_name = request.POST["org_name"]
    org_contact_email = request.POST["org_contact_email"]
    organization = Organization(org_name=org_name, org_contact_email=org_contact_email)
    organization.save()
    return redirect('/organization')

def org_update(request, id):
    organization = Organization.objects.get(id=id)
    template = loader.get_template('org_update.html')
    context = {
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def org_updatesub(request, id):
    organization = Organization.objects.get(id=id)
    organization.org_name = request.POST["org_name"]
    organization.org_contact_email = request.POST["org_contact_email"]
    organization.save()
    return redirect('/organization')

def org_deletesub(request, id):
    organization = Organization.objects.get(id=id)
    organization.delete()
    return redirect('/organization')

def parkinglots(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    parkinglot_list = organization.parkinglots.all()
    template = loader.get_template('parkinglotlist.html')
    context = {
        'organization': organization,
        'parkinglot_list': parkinglot_list,
    }
    return HttpResponse(template.render(context, request))

def parkinglot_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    template = loader.get_template('parkinglot_create.html')
    context = {'organization': organization}
    return HttpResponse(template.render(context, request))

def parkinglot_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    name = request.POST["name"]
    address = request.POST["address"]
    parkinglot = ParkingLot(organization=organization, name=name, address=address)
    parkinglot.save()
    return redirect(f'/organization/{org_id}/parkinglots')

def parkinglot_update(request, org_id, pl_id):
    organization = get_object_or_404(Organization, id=org_id)
    parkinglot = get_object_or_404(ParkingLot, id=pl_id)
    template = loader.get_template('parkinglot_update.html')
    context = {
        'organization': organization,
        'parkinglot': parkinglot,
    }
    return HttpResponse(template.render(context, request))

def parkinglot_updatesub(request, org_id, pl_id):
    parkinglot = get_object_or_404(ParkingLot, id=pl_id)
    parkinglot.name = request.POST["name"]
    parkinglot.address = request.POST["address"]
    parkinglot.save()
    return redirect(f'/organization/{org_id}/parkinglots')

def parkinglot_deletesub(request, org_id, pl_id):
    parkinglot = get_object_or_404(ParkingLot, id=pl_id)
    parkinglot.delete()
    return redirect(f'/organization/{org_id}/parkinglots')

def warehouseinventory_list(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    inventory_list = organization.inventory.all()
    template = loader.get_template('warehouseinventorylist.html')
    context = {
        'organization': organization,
        'inventory_list': inventory_list,
    }
    return HttpResponse(template.render(context, request))

def warehouseinventory_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    parkinglots = ParkingLot.objects.filter(organization=organization)
    vehicles = vehicle.objects.all()
    template = loader.get_template('warehouseinventory_create.html')
    context = {
        'organization': organization,
        'parkinglots': parkinglots,
        'vehicles': vehicles,
    }
    return HttpResponse(template.render(context, request))

def warehouseinventory_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouse_id = request.POST["warehouse"]
    vehicle_id = request.POST["vehicle"]
    date_of_purchase = request.POST["date_of_purchase"]
    cost_of_purchase = request.POST["cost_of_purchase"]
    count = int(request.POST["count"])

    warehouse = get_object_or_404(ParkingLot, id=warehouse_id)
    vehicle_instance = get_object_or_404(vehicle, id=vehicle_id)

    if count < 0:
        raise ValidationError("Count cannot be less than 0.")

    inventory = WarehouseInventory(
        organization=organization,
        warehouse=warehouse,
        vehicle=vehicle_instance,
        date_of_purchase=date_of_purchase,
        cost_of_purchase=cost_of_purchase,
        count=count
    )
    inventory.save()
    return redirect(f'/organization/{org_id}/warehouseinventory')

def warehouseinventory_update(request, org_id, inventory_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouseinventory  = get_object_or_404(WarehouseInventory, id=inventory_id)
    parkinglots = ParkingLot.objects.filter(organization=organization)
    vehicles = vehicle.objects.all()
    template = loader.get_template('warehouseinventory_update.html')
    context = {
        'organization': organization,
        'warehouseinventory': warehouseinventory ,
        'parkinglots': parkinglots,
        'vehicles': vehicles,
    }
    return HttpResponse(template.render(context, request))

def warehouseinventory_updatesub(request, org_id, inventory_id):
    inventory = get_object_or_404(WarehouseInventory, id=inventory_id)
    inventory.warehouse_id = request.POST["warehouse"]
    inventory.vehicle_id = request.POST["vehicle"]
    inventory.date_of_purchase = request.POST["date_of_purchase"]
    inventory.cost_of_purchase = request.POST["cost_of_purchase"]
    count = int(request.POST["count"])

    if count < 0:
        raise ValidationError("Count cannot be less than 0.")
    
    inventory.count = count

    inventory.save()
    return redirect(f'/organization/{org_id}/warehouseinventory')

def warehouseinventory_deletesub(request, org_id, inventory_id):
    inventory = get_object_or_404(WarehouseInventory, id=inventory_id)
    inventory.delete()
    return redirect(f'/organization/{org_id}/warehouseinventory')

def additionalreport(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    report = WarehouseInventory.objects.filter(organization=organization).values('vehicle__name').annotate(total_count=Sum('count'))
    total_vehicles = report.count()
    total_count_sum = report.aggregate(Sum('total_count'))['total_count__sum']
    template = loader.get_template('additionalreport.html')
    context = {
        'organization': organization,
        'report': report,
        'total_vehicles': total_vehicles,
        'total_count_sum': total_count_sum
    }
    return HttpResponse(template.render(context, request))

def transaction_report(request, organization_id):
    organization = Organization.objects.get(id=organization_id)
    transactions = Transaction.objects.filter(organization=organization)
    return render(request, 'transaction_report.html', {'transactions': transactions, 'organization':organization})

from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from vehicles.serializers import vehicleSerializer, OrganizationSerializer, ParkingLotSerializer, WarehouseInventorySerializer

  
class vehicleView(APIView):    
    def get(self, request, *args, **kwargs):  
        result = vehicle.objects.all()  
        serializers = vehicleSerializer(result, many=True)  
        return Response({'status': 'success', "vehicle":serializers.data}, status=200)  
    def post(self, request):  
        serializer = vehicleSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  
        
class OrganizationView(APIView):
    def get(self, request, *args, **kwargs):
        result = Organization.objects.all()
        serializers = OrganizationSerializer(result, many=True)
        return Response({'status': 'success', "organizations": serializers.data}, status=200)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class ParkingLotView(APIView):
    def get(self, request, *args, **kwargs):
        result = ParkingLot.objects.all()
        serializers = ParkingLotSerializer(result, many=True)
        return Response({'status': 'success', "parkinglots": serializers.data}, status=200)

    def post(self, request):
        serializer = ParkingLotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class WarehouseInventoryView(APIView):
    def get(self, request, *args, **kwargs):
        result = WarehouseInventory.objects.all()
        serializers = WarehouseInventorySerializer(result, many=True)
        return Response({'status': 'success', "warehouseinventories": serializers.data}, status=200)

    def post(self, request):
        serializer = WarehouseInventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)