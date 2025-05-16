from rest_framework import serializers
from .models import User
from project_management.models import Department,Designation,Teams, Roles
from project_management.serializers import DepartmentSerializer, DesignationSerializer, TeamsSerializer, RolesSerializer

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, write_only=True)

    role = RolesSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Roles.objects.all(), source='role', write_only=True, required=False
    )

    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source='department', write_only=True, required=False
    )

    designation = DesignationSerializer(read_only=True)
    designation_id = serializers.PrimaryKeyRelatedField(
        queryset=Designation.objects.all(), source='designation', write_only=True, required=False
    )

    team = TeamsSerializer(read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Teams.objects.all(), source='team', write_only=True, required=False
    )

    reporting_manager = serializers.SerializerMethodField()
    reporting_manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reporting_manager', write_only=True, required=False
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'role', 'role_id', 'is_admin', 'employee_name', 'employee_code',
            'department', 'department_id',
            'designation', 'designation_id',
            'team', 'team_id',
            'reporting_manager', 'reporting_manager_id',
            'last_login', 'is_superuser', 'first_name', 'last_name',
            'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions','profile_image'
        ]

    def get_reporting_manager(self, obj):
        if obj.reporting_manager:
            return {
                "id": obj.reporting_manager.id,
                "employee_name": obj.reporting_manager.employee_name,
                "email": obj.reporting_manager.email
            }
        return None



class UserMinimalSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'employee_name', 'team_name']

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField()