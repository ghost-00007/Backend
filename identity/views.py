from django.shortcuts import render

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist 

from .serializers import AppDetailsSerializer,ModuleDetailsSerializer,ComponentDetailsSerializer1,RolesSerializer,RolePermissionSerializer,ModuleWithComponentsSerializer
from .models import AppDetails,ModuleDetails,ComponentDetails,Roles,RolePermission

# Create your views here.
class AppDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app_name = request.data.get("app_name")
        domain = request.data.get("domain")
        version = request.data.get("version")
        release_date = request.data.get("release_date")
        release_note = request.data.get("release_note")

        data = {
            "app_name": app_name,
            "domain": domain,
            "version": version,
            "release_date": release_date,
            "release_note": release_note,
        }

        serializer = AppDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "APP details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add APP details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ModuleDetailsView(APIView):

    def post(self, request):
        app = request.data.get("app")
        module_name = request.data.get("module_name")

        data = {
            "app": app,
            "module_name": module_name,
        }

        serializer = ModuleDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "module details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "module add Department details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class ComponentDetailsView(APIView):

    def post(self, request):
        component_name = request.data.get("component_name")
        app = request.data.get("app")
        module = request.data.get("module")

        data = {
            "component_name": component_name,
            "app": app,
            "module": module,
        }

        serializer = ComponentDetailsSerializer1(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Component details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed add Component details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class RolesView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        description = request.data.get("description")

        data = {
            "role": role,
            "description": description,
        }

        serializer = RolesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Roles details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Roles details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            roles = get_object_or_404(Roles, pk=pk)
            serializer = RolesSerializer(roles)
            data = serializer.data
        else:
            roles = Roles.objects.all()
            serializer = RolesSerializer(roles, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        roles = get_object_or_404(Roles, pk=pk)
        role = request.data.get("role", roles.role)
        description = request.data.get("description", roles.description)

        data = {
            "role": role,
            "description": description,
        }

        serializer = RolesSerializer(roles, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Roles details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Roles details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        roles = get_object_or_404(Roles, pk=pk)
        roles.delete()
        return Response({
            "status": True,
            "message": "Roles deleted successfully."
        }, status=status.HTTP_200_OK)
    
class ComponentList(APIView):
    def post(self, request):
        role_id = request.data.get("role_id")

        if not role_id:
            return Response({
                "status": False,
                "message": "role_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        permissions = RolePermission.objects.filter(role_id=role_id)
        component_permission_map = {
            (p.module_id, p.component_id): {
                "id": p.id,
                "can_access": p.can_access
            } for p in permissions
        }

        modules = ModuleDetails.objects.all()
        data = []

        for module in modules:
            components = ComponentDetails.objects.filter(module=module)
            component_data = []
            module_has_permission = False

            for comp in components:
                key = (module.id, comp.id)
                permission = component_permission_map.get(key)

                if permission:
                    role_permission_id = permission["id"]
                    can_access = permission["can_access"]
                    if can_access:
                        module_has_permission = True
                else:
                    role_permission_id = None
                    can_access = False

                component_data.append({
                    "component_id": comp.id,
                    "component_name": comp.component_name,
                    "Rolepermission": can_access,
                    "role_permission_id": role_permission_id
                })

            data.append({
                "app_id": module.app.id if module.app else None,
                "app_name": module.app.app_name if module.app else "",
                "module_id": module.id,
                "module_name": module.module_name,
                "modulepermission": module_has_permission,
                "component": component_data
            })

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)
       
class RolePermissionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data_list = request.data

        if not isinstance(data_list, list):
            return Response({
                "status": False,
                "message": "Invalid data format. Expected a list of role permissions."
            }, status=status.HTTP_400_BAD_REQUEST)

        success_data = []
        error_data = []

        for data in data_list:
            role = data.get("role")
            app = data.get("app")
            module = data.get("module")
            component = data.get("component")
            can_access = data.get("can_access")
            record_id = data.get("id")

            # Check if all required fields are present
            if not all([role, app, module, component, can_access is not None]):
                error_data.append({
                    "input": data,
                    "errors": "Missing required fields."
                })
                continue

            try:
                if record_id:
                    # Update by ID if provided
                    instance = RolePermission.objects.get(id=record_id)
                    serializer = RolePermissionSerializer(instance, data=data, partial=True)
                else:
                    # Always create a new record if ID is not provided
                    serializer = RolePermissionSerializer(data=data)

                if serializer.is_valid():
                    serializer.save()
                    success_data.append(serializer.data)
                else:
                    error_data.append({
                        "input": data,
                        "errors": serializer.errors
                    })

            except ObjectDoesNotExist:
                error_data.append({
                    "input": data,
                    "errors": "Record with given ID not found."
                })

        return Response({
            "status": True,
            "message": "Processed role permissions",
            "success": success_data,
            "errors": error_data
        }, status=status.HTTP_200_OK)