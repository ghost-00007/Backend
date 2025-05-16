from django.urls import path
from . import views 

urlpatterns = [
    path('appdetails/', views.AppDetailsView.as_view(), name='App-Details-View'), 

    path('moduledetails/', views.ModuleDetailsView.as_view(), name='Module-Details-View'), 

    path('componentdetails/', views.ComponentDetailsView.as_view(), name='Component-Details-View'), 

    path('componentlist/', views.ComponentList.as_view(), name='Component-List'), 

    path('roles/', views.RolesView.as_view(), name='Roles-View'), 
    path('roles/<int:pk>/', views.RolesView.as_view(), name='Roles-View'),

    path('rolepermission/', views.RolePermissionView.as_view(), name='Role-Permission'), 
    path('rolepermission/<int:pk>/', views.RolePermissionView.as_view(), name='Role-Permission'),

   

]