from rest_framework  import serializers
from .models import AppDetails,ModuleDetails,ComponentDetails,Roles,RolePermission



class AppDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppDetails  
        fields = '__all__'

class ModuleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleDetails  
        fields = '__all__'

class ComponentDetailsSerializer1(serializers.ModelSerializer):
    class Meta:
        model = ComponentDetails  
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roles  
        fields = ['id', 'role', 'description']

# class RolePermissionSerializer(serializers.ModelSerializer):
#     role = serializers.CharField(source='role.role', read_only=True)
#     app = serializers.CharField(source='app.app_name', read_only=True)
#     module = serializers.CharField(source='module.module_name', read_only=True)
#     component = serializers.CharField(source='component.component_name', read_only=True)
#     class Meta:
#         model = RolePermission  
#         fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    # Read-only fields for display
    role_name = serializers.CharField(source='role.role', read_only=True)
    app_name = serializers.CharField(source='app.app_name', read_only=True)
    module_name = serializers.CharField(source='module.module_name', read_only=True)
    component_name = serializers.CharField(source='component.component_name', read_only=True)

    # Write-only fields to accept input
    role = serializers.PrimaryKeyRelatedField(queryset=Roles.objects.all(), write_only=True)
    app = serializers.PrimaryKeyRelatedField(queryset=AppDetails.objects.all(), write_only=True)
    module = serializers.PrimaryKeyRelatedField(queryset=ModuleDetails.objects.all(), write_only=True)
    component = serializers.PrimaryKeyRelatedField(queryset=ComponentDetails.objects.all(), write_only=True)

    class Meta:
        model = RolePermission
        fields = [
            'id',
            'can_access',
            # Write-only input fields
            'role', 'app', 'module', 'component',
            # Read-only display fields
            'role_name', 'app_name', 'module_name', 'component_name',
        ]



class ComponentDetailsSerializer(serializers.ModelSerializer):
    component_id = serializers.IntegerField(source='id')

    class Meta:
        model = ComponentDetails
        fields = ['component_id', 'component_name']


class ModuleWithComponentsSerializer(serializers.ModelSerializer):
    App_id = serializers.IntegerField(source='app.id')
    app_name = serializers.CharField(source='app.app_name')
    module_id = serializers.IntegerField(source='id')
    component = serializers.SerializerMethodField()

    class Meta:
        model = ModuleDetails
        fields = ['App_id', 'app_name', 'module_id', 'module_name', 'component']

    def get_component(self, obj):
        components = ComponentDetails.objects.filter(module=obj)
        return ComponentDetailsSerializer(components, many=True).data
