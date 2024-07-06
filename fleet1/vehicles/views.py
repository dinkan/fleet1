from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404

# Create your views here.

from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Hello world!")

from django.template import loader

from .models import vehicle, Organization, ParkingLot, WarehouseInventory, Transaction, Fuel, VehicleFuel, EmissionTarget, FleetDemand, DistanceTravelled, CostProfile, Depot, VehiclesList

from django.db.models import Sum

from django.core.exceptions import ValidationError

from django.utils.dateparse import parse_datetime

from decimal import Decimal, ROUND_HALF_UP

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
    fuel_counts = (
        VehicleFuel.objects
        .filter(vehicle_id__vehicle_inventory__organization=organization)
        .values('fuel__fuel_type','fuel__year')
        .annotate(vehicle_count=Sum('vehicle_id__vehicle_inventory__count'))
        .order_by('fuel__fuel_type')
    )
    transactions = Transaction.objects.filter(organization=organization)
    total_expense = transactions.aggregate(Sum('expense'))['expense__sum'] or 0.0
    total_income = transactions.aggregate(Sum('income'))['income__sum'] or 0.0
    template = loader.get_template('org_details.html')
    context = {
        'organization': organization,
        'fuel_counts': fuel_counts,
        'total_expense': total_expense,
        'total_income': total_income,
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

def fuels(request):
    fuellist = Fuel.objects.all().values()
    template = loader.get_template('fuellist.html')
    context = {
        'fuellist': fuellist,
    }
    return HttpResponse(template.render(context, request))

def fuel_update(request, id):
    fuel = get_object_or_404(Fuel, id=id)
    template = loader.get_template('fuel_update.html')
    context = {
        'fuel': fuel,
    }
    return HttpResponse(template.render(context, request))

def fuel_updatesub(request, id):
    fuel = get_object_or_404(Fuel, id=id)
    fuel.fuel_type = request.POST["fuel_type"]
    fuel.year = request.POST["year"]
    fuel.emissions_per_unit_fuel = request.POST["emissions_per_unit_fuel"]
    fuel.cost_per_unit_fuel = request.POST["cost_per_unit_fuel"]
    fuel.cost_uncertainty = request.POST["cost_uncertainty"]
    fuel.save()
    response = redirect('fuels')
    return response 

def fuel_deletesub(request, id):
    fuel = get_object_or_404(Fuel, id=id)
    fuel.delete()
    response = redirect('fuels')
    return response  

def fuel_create(request):
    template = loader.get_template('fuel_create.html')
    context = {}
    return HttpResponse(template.render(context, request))

def fuel_createsub(request):
    fuel_type = request.POST["fuel_type"]
    year = request.POST["year"]
    emissions_per_unit_fuel = request.POST["emissions_per_unit_fuel"]
    cost_per_unit_fuel = request.POST["cost_per_unit_fuel"]
    cost_uncertainty = request.POST["cost_uncertainty"]
    fuel = Fuel(fuel_type=fuel_type, year=year, emissions_per_unit_fuel=emissions_per_unit_fuel, cost_per_unit_fuel=cost_per_unit_fuel, cost_uncertainty=cost_uncertainty)
    fuel.save()
    response = redirect('fuels')
    return response

def vehicle_fuels(request):
    vehiclefuellist = VehicleFuel.objects.all()

    template = loader.get_template('vehiclefuellist.html')
    context = {
        'vehiclefuellist': vehiclefuellist,
    }
    return HttpResponse(template.render(context, request))

def vehicle_fuel_update(request, id):
    vehicle_fuel = get_object_or_404(VehicleFuel, id=id)
    template = loader.get_template('vehicle_fuel_update.html')
    context = {
        'vehicle_fuel': vehicle_fuel,
        'vehicles': vehicle.objects.all(),
        'fuels': Fuel.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def vehicle_fuel_updatesub(request, id):
    vehicle_fuel = get_object_or_404(VehicleFuel, id=id)
    vehicle_fuel.vehicle_id = get_object_or_404(vehicle, id=request.POST["vehicle_id"])
    vehicle_fuel.fuel = get_object_or_404(Fuel, id=request.POST["fuel"])
    vehicle_fuel.consumption_per_km = request.POST["consumption_per_km"]
    vehicle_fuel.save()
    response = redirect('/vehicle_fuels')
    return response  

def vehicle_fuel_deletesub(request, id):
    vehicle_fuel = get_object_or_404(VehicleFuel, id=id)
    vehicle_fuel.delete()
    response = redirect('/vehicle_fuels')
    return response  

def vehicle_fuel_create(request):
    template = loader.get_template('vehicle_fuel_create.html')
    context = {
        'vehicles': vehicle.objects.all(),
        'fuels': Fuel.objects.all(),
    }
    return HttpResponse(template.render(context, request))

def vehicle_fuel_createsub(request):
    vehicle_id = get_object_or_404(vehicle, id=request.POST["vehicle_id"])
    fuel_id = get_object_or_404(Fuel, id=request.POST["fuel_id"])
    consumption_per_km = request.POST["consumption_per_km"]
    vehicle_fuel = VehicleFuel(vehicle_id=vehicle_id, fuel=fuel_id, consumption_per_km=consumption_per_km)
    vehicle_fuel.save()
    response = redirect('/vehicle_fuels')
    return response

def emission_target_list(request, org_id):
    emission_target_list = EmissionTarget.objects.filter(organization_id=org_id)
    organization = get_object_or_404(Organization, id=org_id)
    template = loader.get_template('emissiontargetlist.html')
    context = {
        'emission_target_list': emission_target_list,
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def emission_target_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    template = loader.get_template('emissiontarget_create.html')
    context = {
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def emission_target_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    year = request.POST["year"]
    carbon_emission = request.POST["carbon_emission"]
    emission_target = EmissionTarget(organization=organization, year=year, carbon_emission=carbon_emission)
    emission_target.save()
    return redirect(f'/emissiontargetlist/{org_id}')

def emission_target_update(request, id):
    emission_target = get_object_or_404(EmissionTarget, id=id)
    template = loader.get_template('emissiontarget_update.html')
    context = {
        'emission_target': emission_target,
    }
    return HttpResponse(template.render(context, request))

def emission_target_updatesub(request, id):
    emission_target = get_object_or_404(EmissionTarget, id=id)
    emission_target.year = request.POST["year"]
    emission_target.carbon_emission = request.POST["carbon_emission"]
    emission_target.save()
    return redirect(f'/emissiontargetlist/{emission_target.organization.id}')

def emission_target_deletesub(request, id):
    emission_target = get_object_or_404(EmissionTarget, id=id)
    org_id = emission_target.organization.id
    emission_target.delete()
    return redirect(f'/emissiontargetlist/{org_id}')

def fleet_demand_list(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    fleet_demands = FleetDemand.objects.filter(organization=organization).values()
    template = loader.get_template('fleetdemand_list.html')
    context = {
        'organization': organization,
        'fleet_demands': fleet_demands,
    }
    return HttpResponse(template.render(context, request))

def fleet_demand_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    template = loader.get_template('fleetdemand_create.html')
    context = {
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def fleet_demand_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    year = request.POST["year"]
    size = request.POST["size"]
    distance = request.POST["distance"]
    demand = request.POST["demand"]
    fleet_demand = FleetDemand(organization=organization, year=year, size=size, distance=distance, demand=demand)
    fleet_demand.save()
    return redirect('fleet_demand_list', org_id=org_id)

def fleet_demand_update(request, id):
    fleet_demand = get_object_or_404(FleetDemand, id=id)
    template = loader.get_template('fleetdemand_update.html')
    context = {
        'fleet_demand': fleet_demand,
    }
    return HttpResponse(template.render(context, request))

def fleet_demand_updatesub(request, id):
    fleet_demand = get_object_or_404(FleetDemand, id=id)
    fleet_demand.year = request.POST["year"]
    fleet_demand.size = request.POST["size"]
    fleet_demand.distance = request.POST["distance"]
    fleet_demand.demand = request.POST["demand"]
    fleet_demand.save()
    return redirect('fleet_demand_list', org_id=fleet_demand.organization.id)

def fleet_demand_deletesub(request, id):
    fleet_demand = get_object_or_404(FleetDemand, id=id)
    org_id = fleet_demand.organization.id
    fleet_demand.delete()
    return redirect('fleet_demand_list', org_id=org_id)

def distancetravelledlist(request, org_id, inventory_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouseinventory  = get_object_or_404(WarehouseInventory, id=inventory_id)
    distancetravelled_list = DistanceTravelled.objects.filter(vehicle_id=warehouseinventory)
    template = loader.get_template('distancetravelledlist.html')
    context = {
        'organization': organization,
        'warehouseinventory': warehouseinventory,
        'distancetravelled_list':distancetravelled_list
    }
    return HttpResponse(template.render(context, request))

def distance_travelled_details(request, org_id, inventory_id, distance_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouseinventory  = get_object_or_404(WarehouseInventory, id=inventory_id)
    distance_travelled = get_object_or_404(DistanceTravelled, id=distance_id)

    consumption_per_km = distance_travelled.fuel_used.consumption_per_km
    emissions_per_unit_fuel = distance_travelled.fuel_used.fuel.emissions_per_unit_fuel
    carbon_emission = distance_travelled.distance_travelled * consumption_per_km * emissions_per_unit_fuel
    
    template = loader.get_template('distance_travelled_details.html')
    context = {
        'organization': organization,
        'warehouseinventory': warehouseinventory,
        'distance_travelled': distance_travelled,
        'carbon_emission': carbon_emission
    }
    return HttpResponse(template.render(context, request))

def distance_travelled_create(request, org_id, inventory_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouseinventory  = get_object_or_404(WarehouseInventory, id=inventory_id)
    vehicle = warehouseinventory.vehicle
    vehicle_fuels = VehicleFuel.objects.filter(vehicle_id=vehicle)

    template = loader.get_template('distance_travelled_create.html')
    context = {
        'organization': organization,
        'warehouseinventory': warehouseinventory,
        'vehicle_fuels': vehicle_fuels, 
    }
    return HttpResponse(template.render(context, request))

def distance_travelled_createsub(request, org_id, inventory_id):
    warehouseinventory  = get_object_or_404(WarehouseInventory, id=inventory_id)

    date = request.POST["date"]
    distance_travelled = request.POST["distance_travelled"]
    fuel_used_id = request.POST["fuel_used"]

    distance_travelled = float(distance_travelled)
    fuel_used = get_object_or_404(VehicleFuel, id=fuel_used_id)

    new_distance_travelled = DistanceTravelled(
        vehicle_id=warehouseinventory,
        date=date,
        distance_travelled=distance_travelled,
        fuel_used=fuel_used
    )
    new_distance_travelled.save()

    return redirect(f'/organization/{org_id}/warehouseinventory/{inventory_id}/distancetravelledlist')
    
def distance_travelled_update(request, org_id, inventory_id, distance_id):
    organization = get_object_or_404(Organization, id=org_id)
    warehouseinventory = get_object_or_404(WarehouseInventory, id=inventory_id)
    distance_travelled = get_object_or_404(DistanceTravelled, id=distance_id)

    vehicle_fuels = VehicleFuel.objects.filter(vehicle_id=warehouseinventory.vehicle)

    template = loader.get_template('distance_travelled_update.html')
    context = {
        'organization': organization,
        'warehouseinventory': warehouseinventory,
        'distance_travelled': distance_travelled,
        'vehicle_fuels': vehicle_fuels,
    }
    return HttpResponse(template.render(context, request))

def distance_travelled_updatesub(request, org_id, inventory_id, distance_id):
    distance_travelled = get_object_or_404(DistanceTravelled, id=distance_id)

    distance_travelled.date = request.POST["date"]
    distance_travelled.distance_travelled = request.POST["distance_travelled"]
    distance_travelled.fuel_used_id = request.POST["fuel_used"]

    distance_travelled.save()
    return redirect(f'/organization/{org_id}/warehouseinventory/{inventory_id}/distancetravelledlist')

def distance_travelled_deletesub(request, org_id, inventory_id, distance_id):
    distance_travelled = get_object_or_404(DistanceTravelled, id=distance_id)
    distance_travelled.delete()
    return redirect(f'/organization/{org_id}/warehouseinventory/{inventory_id}/distancetravelledlist')

def transactionslist(request, id):
    organization = get_object_or_404(Organization, id=id)
    transactions_list = Transaction.objects.filter(organization=organization)
    template = loader.get_template('transactionslist.html')
    context = {
        'organization': organization,
        'transactions_list': transactions_list
    }
    return HttpResponse(template.render(context, request))

def transactions_create(request, id):
    organization = get_object_or_404(Organization, id=id)
    inventory_items = WarehouseInventory.objects.filter(organization=organization)
    template = loader.get_template('transactions_create.html')
    context = {
        'organization': organization,
        'inventory_items': inventory_items,
    }
    return HttpResponse(template.render(context, request))

def transactions_createsub(request, id):
    organization = get_object_or_404(Organization, id=id)
    date_str = request.POST["date"]
    date = parse_datetime(date_str)
    details = request.POST["details"]
    expense = float(request.POST["expense"])
    income = float(request.POST["income"])
    reference_id = request.POST.get("reference_id")
    
    reference = None
    if reference_id and reference_id != "None":
        reference = get_object_or_404(WarehouseInventory, id=reference_id)
    
    transaction = Transaction(
        organization=organization,
        date=date,
        details=details,
        expense=expense,
        income=income,
        reference_id=reference
    )
    transaction.save()
    return redirect(f'/org_details/{id}/transactionslist')

def transactions_update(request, id, transaction_id):
    organization = get_object_or_404(Organization, id=id)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    inventory_items = WarehouseInventory.objects.filter(organization=organization)
    template = loader.get_template('transactions_update.html')
    context = {
        'organization': organization,
        'transaction': transaction,
        'inventory_items': inventory_items,
    }
    return HttpResponse(template.render(context, request))

def transactions_updatesub(request, id, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.date = request.POST["date"]
    transaction.details = request.POST["details"]
    transaction.expense = float(request.POST["expense"])
    transaction.income = float(request.POST["income"])
    reference_id = request.POST.get("reference_id")
    
    if reference_id:
        transaction.reference_id = get_object_or_404(WarehouseInventory, id=reference_id)
    else:
        transaction.reference_id = None
    
    transaction.save()
    return redirect(f'/org_details/{id}/transactionslist')

def transactions_deletesub(request, id, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect(f'/org_details/{id}/transactionslist')

def costprofilelist(request, id):
    organization = get_object_or_404(Organization, id=id)
    costprofile_list = CostProfile.objects.filter(organization=organization)
    template = loader.get_template('costprofilelist.html')
    context = {
        'organization': organization,
        'costprofile_list': costprofile_list
    }
    return HttpResponse(template.render(context, request))

def costprofile_create(request, id):
    organization = get_object_or_404(Organization, id=id)
    template = loader.get_template('costprofile_create.html')
    context = {
        'organization': organization,
    }
    return HttpResponse(template.render(context, request))

def costprofile_createsub(request, id):
    organization = get_object_or_404(Organization, id=id)
    end_of_year = request.POST["end_of_year"]
    resale_value_percent = int(request.POST["resale_value_percent"])
    insurance_cost_percent = int(request.POST["insurance_cost_percent"])
    maintenance_cost_percent = int(request.POST["maintenance_cost_percent"])

    if resale_value_percent < 0 or resale_value_percent > 100:
        raise ValidationError("Resale Value must be a % between 0 and 100")
    if insurance_cost_percent < 0 or insurance_cost_percent > 100:
        raise ValidationError("Insurance Cost must be a % between 0 and 100")
    if maintenance_cost_percent < 0 or maintenance_cost_percent > 100:
        raise ValidationError("Maintenance Cost must be a % between 0 and 100")
    
    costprofile = CostProfile(
        organization=organization,
        end_of_year=end_of_year,
        resale_value_percent=resale_value_percent,
        insurance_cost_percent=insurance_cost_percent,
        maintenance_cost_percent=maintenance_cost_percent
    )
    costprofile.save()
    return redirect(f'/org_details/{id}/costprofilelist')

def costprofile_update(request, id, costprofile_id):
    organization = get_object_or_404(Organization, id=id)
    costprofile = get_object_or_404(CostProfile, id=costprofile_id)
    template = loader.get_template('costprofile_update.html')
    context = {
        'organization': organization,
        'costprofile': costprofile,
    }
    return HttpResponse(template.render(context, request))

def costprofile_updatesub(request, id, costprofile_id):
    costprofile = get_object_or_404(CostProfile, id=costprofile_id)
    costprofile.end_of_year = request.POST["end_of_year"]
    resale_value_percent = int(request.POST["resale_value_percent"])
    insurance_cost_percent = int(request.POST["insurance_cost_percent"])
    maintenance_cost_percent = int(request.POST["maintenance_cost_percent"])

    if resale_value_percent < 0 or resale_value_percent > 100:
        raise ValidationError("Resale Value must be a % between 0 and 100")
    if insurance_cost_percent < 0 or insurance_cost_percent > 100:
        raise ValidationError("Insurance Cost must be a % between 0 and 100")
    if maintenance_cost_percent < 0 or maintenance_cost_percent > 100:
        raise ValidationError("Maintenance Cost must be a % between 0 and 100")
    
    costprofile.resale_value_percent = resale_value_percent
    costprofile.insurance_cost_percent = insurance_cost_percent
    costprofile.maintenance_cost_percent = maintenance_cost_percent

    costprofile.save()
    return redirect(f'/org_details/{id}/costprofilelist')

def costprofile_deletesub(request, id, costprofile_id):
    costprofile = get_object_or_404(CostProfile, id=costprofile_id)
    costprofile.delete()
    return redirect(f'/org_details/{id}/costprofilelist')

def depots(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    depot_list = organization.depots.all()
    template = loader.get_template('depotlist.html')
    context = {
        'organization': organization,
        'depot_list': depot_list,
    }
    return HttpResponse(template.render(context, request))

def depot_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    template = loader.get_template('depot_create.html')
    context = {'organization': organization}
    return HttpResponse(template.render(context, request))

def depot_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    name = request.POST["name"]
    address = request.POST["address"]
    parking_capacity = request.POST["parking_capacity"]
    charging_points = request.POST["charging_points"]
    depot = Depot(
        organization=organization,
        name=name,
        address=address,
        parking_capacity=parking_capacity,
        charging_points=charging_points
    )
    depot.save()
    return redirect(f'/organization/{org_id}/depots')

def depot_update(request, org_id, dp_id):
    organization = get_object_or_404(Organization, id=org_id)
    depot = get_object_or_404(Depot, id=dp_id)
    template = loader.get_template('depot_update.html')
    context = {
        'organization': organization,
        'depot': depot,
    }
    return HttpResponse(template.render(context, request))

def depot_updatesub(request, org_id, dp_id):
    depot = get_object_or_404(Depot, id=dp_id)
    depot.name = request.POST["name"]
    depot.address = request.POST["address"]
    depot.parking_capacity = request.POST["parking_capacity"]
    depot.charging_points = request.POST["charging_points"]
    depot.save()
    return redirect(f'/organization/{org_id}/depots')

def depot_deletesub(request, org_id, dp_id):
    depot = get_object_or_404(Depot, id=dp_id)
    depot.delete()
    return redirect(f'/organization/{org_id}/depots')

def vehicles_list(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    vehicles_list = organization.vehicles_list.all()
    vehicles_with_rounded_age = []
    for vehicle in vehicles_list:
        age = vehicle.age
        rounded_age = int(age.to_integral_value(rounding=ROUND_HALF_UP)) + 1
        vehicles_with_rounded_age.append({
            'vehicle': vehicle,
            'rounded_age': rounded_age
        })
    template = loader.get_template('vehicles_list.html')
    context = {
        'organization': organization,
        'vehicles_with_rounded_age': vehicles_with_rounded_age,
    }
    return HttpResponse(template.render(context, request))

def vehicles_list_details(request, org_id, vl_id):
    organization = get_object_or_404(Organization, id=org_id)
    vehicle_entry = get_object_or_404(VehiclesList, id=vl_id)
    age = vehicle_entry.age

    rounded_age = int(age.to_integral_value(rounding=ROUND_HALF_UP)) + 1
    try:
        cost_profile = CostProfile.objects.get(organization=organization, end_of_year=rounded_age)
    except CostProfile.DoesNotExist:
        cost_profile = None

    if cost_profile and cost_profile.end_of_year == rounded_age:
        maintenance_cost_percent = Decimal(cost_profile.maintenance_cost_percent / 100)
        insurance_cost_percent = Decimal(cost_profile.insurance_cost_percent / 100)
        resale_value_percent = Decimal(cost_profile.resale_value_percent / 100)

        proposed_maintenance_cost = vehicle_entry.cost_of_purchase * rounded_age * maintenance_cost_percent
        proposed_insurance_cost = vehicle_entry.cost_of_purchase * rounded_age * insurance_cost_percent
        proposed_resale_value = vehicle_entry.cost_of_purchase * rounded_age * resale_value_percent

        proposed_maintenance_cost = proposed_maintenance_cost.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        proposed_insurance_cost = proposed_insurance_cost.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        proposed_resale_value = proposed_resale_value.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
    else:
        proposed_maintenance_cost = proposed_insurance_cost = proposed_resale_value = None
    
    context = {
        'organization': organization,
        'vehicle_entry': vehicle_entry,
        'proposed_maintenance_cost': proposed_maintenance_cost,
        'proposed_insurance_cost': proposed_insurance_cost,
        'proposed_resale_value': proposed_resale_value,
        'cost_profile': cost_profile,
        'rounded_age':rounded_age
    }
    
    return render(request, 'vehicles_list_details.html', context)

def vehicles_list_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    depots = organization.depots.all()
    warehouses = organization.parkinglots.all()
    vehicles = vehicle.objects.all()
    template = loader.get_template('vehicles_list_create.html')
    context = {
        'organization': organization,
        'depots': depots,
        'warehouses': warehouses,
        'vehicles': vehicles,
    }
    return HttpResponse(template.render(context, request))

def vehicles_list_createsub(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    depot = get_object_or_404(Depot, id=request.POST["depot_id"])
    warehouse = get_object_or_404(ParkingLot, id=request.POST["warehouse_id"])
    vehicle_instance = get_object_or_404(vehicle, id=request.POST["vehicle_id"])
    date_of_purchase = request.POST["date_of_purchase"]
    cost_of_purchase = request.POST["cost_of_purchase"]
    vin_number = request.POST["vin_number"]
    status = request.POST["status"]
    maintenance_cost = request.POST["maintenance_cost"]
    insurance_cost = request.POST["insurance_cost"]
    resale_value = request.POST["resale_value"]
    
    vehicles_list = VehiclesList(
        organization=organization,
        depot=depot,
        warehouse=warehouse,
        vehicle=vehicle_instance,
        date_of_purchase=date_of_purchase,
        cost_of_purchase=cost_of_purchase,
        vin_number=vin_number,
        status=status,
        maintenance_cost=maintenance_cost,
        insurance_cost=insurance_cost,
        resale_value=resale_value
    )
    vehicles_list.save()
    return redirect(f'/organization/{org_id}/vehicles_list')

def vehicles_list_update(request, org_id, vl_id):
    organization = get_object_or_404(Organization, id=org_id)
    vehicles_list = get_object_or_404(VehiclesList, id=vl_id)
    depots = organization.depots.all()
    warehouses = organization.parkinglots.all()
    vehicles = vehicle.objects.all()
    template = loader.get_template('vehicles_list_update.html')
    context = {
        'organization': organization,
        'vehicles_list': vehicles_list,
        'depots': depots,
        'warehouses': warehouses,
        'vehicles': vehicles,
    }
    return HttpResponse(template.render(context, request))

def vehicles_list_updatesub(request, org_id, vl_id):
    vehicles_list = get_object_or_404(VehiclesList, id=vl_id)
    vehicles_list.depot = get_object_or_404(Depot, id=request.POST["depot_id"])
    vehicles_list.warehouse = get_object_or_404(ParkingLot, id=request.POST["warehouse_id"])
    vehicles_list.vehicle = get_object_or_404(vehicle, id=request.POST["vehicle_id"])
    vehicles_list.date_of_purchase = request.POST["date_of_purchase"]
    vehicles_list.cost_of_purchase = request.POST["cost_of_purchase"]
    vehicles_list.vin_number = request.POST["vin_number"]
    vehicles_list.status = request.POST["status"]
    vehicles_list.maintenance_cost = request.POST["maintenance_cost"]
    vehicles_list.insurance_cost = request.POST["insurance_cost"]
    vehicles_list.resale_value = request.POST["resale_value"]
    vehicles_list.save()
    return redirect(f'/organization/{org_id}/vehicles_list')

def vehicles_list_deletesub(request, org_id, vl_id):
    vehicles_list = get_object_or_404(VehiclesList, id=vl_id)
    vehicles_list.delete()
    return redirect(f'/organization/{org_id}/vehicles_list')


from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from vehicles.serializers import vehicleSerializer, OrganizationSerializer, ParkingLotSerializer, WarehouseInventorySerializer, FuelSerializer, VehicleFuelSerializer, EmissionTargetSerializer, FleetDemandSerializer, DistanceTravelledSerializer, TransactionSerializer, CostProfileSerializer, DepotSerializer, VehiclesListSerializer

  
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
        
class FuelView(APIView):    
    def get(self, request, *args, **kwargs):  
        result = Fuel.objects.all()  
        serializers = FuelSerializer(result, many=True)  
        return Response({'status': 'success', "fuel": serializers.data}, status=200)  
    
    def post(self, request):  
        serializer = FuelSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)  

class VehicleFuelView(APIView):    
    def get(self, request, *args, **kwargs):  
        result = VehicleFuel.objects.all()  
        serializers = VehicleFuelSerializer(result, many=True)  
        return Response({'status': 'success', "vehicle_fuel": serializers.data}, status=200)  
    
    def post(self, request):  
        serializer = VehicleFuelSerializer(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)  
        else:  
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class EmissionTargetView(APIView):
    def get(self, request, *args, **kwargs):
        result = EmissionTarget.objects.all()
        serializers = EmissionTargetSerializer(result, many=True)
        return Response({'status': 'success', "emission_targets": serializers.data}, status=200)

    def post(self, request):
        serializer = EmissionTargetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class FleetDemandView(APIView):
    def get(self, request, *args, **kwargs):
        result = FleetDemand.objects.all()
        serializers = FleetDemandSerializer(result, many=True)
        return Response({'status': 'success', "fleet_demands": serializers.data}, status=200)

    def post(self, request):
        serializer = FleetDemandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class DistanceTravelledView(APIView):
    def get(self, request, *args, **kwargs):
        distances = DistanceTravelled.objects.all()
        serializer = DistanceTravelledSerializer(distances, many=True)
        return Response({'status': 'success', 'distances': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DistanceTravelledSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class TransactionView(APIView):
    def get(self, request, *args, **kwargs):
        result = Transaction.objects.all()
        serializer = TransactionSerializer(result, many=True)
        return Response({'status': 'success', 'transactions': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class CostProfileView(APIView):
    def get(self, request, *args, **kwargs):
        result = CostProfile.objects.all()
        serializer = CostProfileSerializer(result, many=True)
        return Response({'status': 'success', 'costprofiles': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = CostProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class DepotView(APIView):
    def get(self, request, *args, **kwargs):
        result = Depot.objects.all()
        serializers = DepotSerializer(result, many=True)
        return Response({'status': 'success', "depots": serializers.data}, status=200)

    def post(self, request):
        serializer = DepotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class VehiclesListView(APIView):
    def get(self, request, *args, **kwargs):
        result = VehiclesList.objects.all()
        serializers = VehiclesListSerializer(result, many=True)
        return Response({'status': 'success', "vehicles_list": serializers.data}, status=200)

    def post(self, request):
        serializer = VehiclesListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)