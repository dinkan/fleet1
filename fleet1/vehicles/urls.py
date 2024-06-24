from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('vehicles', views.vehicles, name='vehicles'),
    path('details/<int:id>', views.details, name='details'),
    path('update/<int:id>', views.update, name='update'),    
    path('updatesub/<int:id>', views.updatesub, name='updatesub'),      
    path('deletesub/<int:id>', views.deletesub, name='deletesub'),          
    path('create', views.create, name='create'),    
    path('createsub',views.createsub, name='createsub'),      
    path('api/', views.vehicleView.as_view())  
]
