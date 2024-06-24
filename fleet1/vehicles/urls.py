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
    path('api/', views.vehicleView.as_view()),
    path('organization', views.organization, name='organization'),
    path('org_details/<int:id>', views.org_details, name='org_details'),
    path('org_create', views.org_create, name='org_create'),
    path('org_createsub', views.org_createsub, name='org_createsub'),
    path('org_update/<int:id>', views.org_update, name='org_update'),
    path('org_updatesub/<int:id>', views.org_updatesub, name='org_updatesub'),
    path('org_deletesub/<int:id>', views.org_deletesub, name='org_deletesub'),
    path('api/organization/', views.OrganizationView.as_view()),
]
