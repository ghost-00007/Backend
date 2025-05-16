from rest_framework  import serializers
from .models import Department,Project,Teams,Designation, PriorityMaster,TaskDetails

from identity.serializers import RolesSerializer
from identity.models import Roles
from users.models import User

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department  
        fields = ['id', 'department_name', 'department_code']


class ProjectSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.employee_name', read_only=True)
    resource_allocation = serializers.JSONField()
    start_date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    end_date = serializers.DateField(format="%d-%m-%Y", input_formats=["%d-%m-%Y"])
    class Meta:
        model = Project  
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True, source='department'
    )
    class Meta:
        model = Designation  
        fields = ['id', 'designation', 'department', 'department_id']

class TeamsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teams  
        fields = '__all__'

class PriorityMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityMaster  
        fields = '__all__'
        
class TaskDetailsSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.project_name', read_only=True)
    assignee_name = serializers.CharField(source='Assignee.employee_name', read_only=True)
    team_name = serializers.CharField(source='teams.team_name', read_only=True)
    task_creater_name = serializers.CharField(source='task_creater.employee_name', read_only=True)
    # stake_holder_name = serializers.CharField(source='stake_holder.employee_name', read_only=True)
    stake_holder = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField()),
        required=False
    )
    
    class Meta:
        model = TaskDetails
        fields = [
            'id',
            'project',
            'project_name',
            'task_title',
            'status',
            'task_describtion',
            'teams',
            'team_name',
            'Assignee',
            'assignee_name',
            'task_creater',
            'task_creater_name',
            'stake_holder',
            'stake_holder',
            'start_date',
            'end_date',
            'actual_start_date',
            'actual_end_date',
            'assigned_hours',
            'actual_hours',
            'priority_level',
            'milestone',
            'sprint',
            'module',
            'attachment',
        ]
        extra_kwargs = {
            'actual_start_date': {'required': False},
            'actual_end_date': {'required': False},
            'actual_hours': {'required': False},
        }
        
    def to_representation(self, instance):
        """Override to add stake_holder user names to output."""
        data = super().to_representation(instance)
        from users.models import User
        result = []
        for item in data.get('stake_holder', []):
            user_id = item.get("user_id")
            try:
                user = User.objects.get(id=user_id)
                result.append({
                    "user_id": user_id,
                    "user_name": user.employee_name
                })
            except User.DoesNotExist:
                result.append({
                    "user_id": user_id,
                    "user_name": None
                })
        data['stake_holder'] = result
        return data



class TaskInfoSerializer(serializers.Serializer):
    tasktile = serializers.CharField(source='task_title')
    duartion = serializers.SerializerMethodField()

    def get_duartion(self, obj):
        if obj.start_date and obj.end_date:
            return str((obj.end_date - obj.start_date).days or 1)
        return "0"

class TaskSerializer(serializers.Serializer):
    tasktile = serializers.CharField()
    duartion = serializers.CharField()
    status = serializers.CharField()
    assigned_hours = serializers.IntegerField()
    assignee_name = serializers.CharField()

class ModuleSerializer(serializers.Serializer):
    modulename = serializers.CharField()
    tasknames = TaskSerializer(many=True)

class SprintSerializer(serializers.Serializer):
    sprints = serializers.CharField()
    tasknames = ModuleSerializer(many=True)

class MilestoneSerializer(serializers.Serializer):
    milestone = serializers.CharField()
    sprints = SprintSerializer(many=True)