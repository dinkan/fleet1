from django.shortcuts import render

from django.shortcuts import redirect

# Create your views here.

from django.http import HttpResponse

def welcome(request):
    return HttpResponse("Hello world!")

from django.template import loader

from .models import vehicle

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
  mymember = vehicle(vehnumber=vehnumber,name=name)
  mymember.save()
  response = redirect('/vehicles')
  return response


from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from vehicles.serializers import vehicleSerializer  

  
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
