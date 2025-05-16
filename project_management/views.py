from functools import partial
from collections import defaultdict
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
from django.utils import timezone
from .serializers import DepartmentSerializer,ProjectSerializer,TeamsSerializer,DesignationSerializer, PriorityMasterSerializer, TaskDetailsSerializer , MilestoneSerializer
from .models import Department,Project,Teams,Designation, PriorityMaster, TaskDetails
from users.models import User
from datetime import date
import json
# from users.serializers import UserSerializer
# from users.views import IsSuperUser
# from users.models import User


class DepartmentView(APIView):
    permission_classes = [IsAuthenticated]

class DepartmentView(APIView):  # Assuming you're using APIView
    def post(self, request):
        department_code = request.data.get("department_code")
        department_name = request.data.get("department_name")

        if department_name:
            department_name = "_".join(word.capitalize() for word in department_name.strip().split())

        if department_code:
            department_code = department_code.strip().upper()

        data = {
            "department_code": department_code,
            "department_name": department_name,
        }

        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Department details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Department details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            department = get_object_or_404(Department, pk=pk)
            serializer = DepartmentSerializer(department)
            data = serializer.data
        else:
            departments = Department.objects.all()
            serializer = DepartmentSerializer(departments, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department_code = request.data.get("department_code", department.department_code)
        department_name = request.data.get("department_name", department.department_name)

        data = {
            "department_code": department_code,
            "department_name": department_name,
        }

        serializer = DepartmentSerializer(department, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Department details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Department details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response({
            "status": True,
            "message": "Department deleted successfully."
        }, status=status.HTTP_200_OK)
    
class ProjectView(APIView):
    permission_classes = [IsAuthenticated]

    # POST method to create a project
    def post(self, request):
        # Extracting the project details from the request data
        project_code = request.data.get("project_code")
        project_name = request.data.get("project_name")
        description = request.data.get("description")
        manager = request.data.get("manager")
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        milestone = request.data.get("milestone")
        budget = request.data.get("budget")
        resource_allocation = request.data.get("resource_allocation")

        # Capitalize project_name
        if project_name:
            project_name = " ".join(word.capitalize() for word in project_name.strip().split())

        # Ensure resource_allocation is parsed as a JSON array (if it's a string)
        if isinstance(resource_allocation, str):
            try:
                resource_allocation = json.loads(resource_allocation)
            except json.JSONDecodeError:
                return Response({
                    "status": False,
                    "message": "Invalid JSON format for resource allocation.",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicate project name (case-insensitive)
        if Project.objects.filter(project_name__iexact=project_name).exists():
            return Response({
                "status": False,
                "message": "Project with this name already exists.",
                "data": {}
            }, status=status.HTTP_200_OK)

        # Prepare data for saving
        data = {
            "project_code": project_code,
            "project_name": project_name,
            "description": description,
            "manager": manager,
            "start_date": start_date,
            "end_date": end_date,
            "milestone": milestone,
            "budget": budget,
            "resource_allocation": resource_allocation,  # Ensure valid JSON
        }

        # Serialize and save the project
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Project details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Project details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # GET method to retrieve project(s)
    def get(self, request, pk=None):
        if pk:
            project = get_object_or_404(Project, pk=pk)
            serializer = ProjectSerializer(project)
            data = serializer.data
        else:
            project = Project.objects.all()
            serializer = ProjectSerializer(project, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    # PUT method to update project details
    def put(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project_code = request.data.get("project_code", project.project_code)
        project_name = request.data.get("project_name", project.project_name)
        description = request.data.get("description", project.description)
        manager = request.data.get("manager", project.manager)
        start_date = request.data.get("start_date", project.start_date)
        end_date = request.data.get("end_date", project.end_date)
        milestone = request.data.get("milestone", project.milestone)
        budget = request.data.get("budget", project.budget)
        resource_allocation = request.data.get("resource_allocation", project.resource_allocation)

        # Ensure resource_allocation is parsed as a JSON array (if it's a string)
        if isinstance(resource_allocation, str):
            try:
                resource_allocation = json.loads(resource_allocation)
            except json.JSONDecodeError:
                return Response({
                    "status": False,
                    "message": "Invalid JSON format for resource allocation.",
                    "data": {}
                }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "project_code": project_code,
            "project_name": project_name,
            "description": description,
            "manager": manager,
            "start_date": start_date,
            "end_date": end_date,
            "milestone": milestone,
            "budget": budget,
            "resource_allocation": resource_allocation,
        }

        serializer = ProjectSerializer(project, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Project details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Project details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a project
    def delete(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response({
            "status": True,
            "message": "Project deleted successfully."
        }, status=status.HTTP_200_OK)
class TeamsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team_name = request.data.get("team_name")

        if team_name:
            team_name = " ".join(word.capitalize() for word in team_name.strip().split())

        data = {
            "team_name": team_name,
        }

        serializer = TeamsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Teams details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Team with same name already exists.",
            "data": serializer.errors
        }, status=status.HTTP_200_OK)

    def get(self, request, pk=None):
        if pk:
            teams = get_object_or_404(Teams, pk=pk)
            serializer = TeamsSerializer(teams)
            data = serializer.data
        else:
            teams = Teams.objects.all()
            serializer = TeamsSerializer(teams, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        teams = get_object_or_404(Teams, pk=pk)
        team_name = request.data.get("team_name", teams.team_name)

        data = {
            "team_name": team_name,
        }

        serializer = TeamsSerializer(teams, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Teams details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Teams details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        teams = get_object_or_404(Teams, pk=pk)
        teams.delete()
        return Response({
            "status": True,
            "message": "Teams deleted successfully."
        }, status=status.HTTP_200_OK)
    
class DesignationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        department = request.data.get("department_id")
        designation = request.data.get("designation")

        data = {
            "department_id": department,
            "designation": designation,
        }

        serializer = DesignationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Designation details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        
        # Return actual validation error messages
        return Response({
            "status": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            designation = get_object_or_404(Designation, pk=pk)
            serializer = DesignationSerializer(designation)
            data = serializer.data
        else:
            designation = Designation.objects.all()
            serializer = DesignationSerializer(designation, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        designation_instance = get_object_or_404(Designation, pk=pk)

        # Use provided value or fallback to existing one
        department_id = request.data.get("department_id")
        department = get_object_or_404(Department, pk=department_id) if department_id else designation_instance.department

        designation_name = request.data.get("designation", designation_instance.designation)

        data = {
            "department_id": department.id,
            "designation": designation_name,
        }

        serializer = DesignationSerializer(designation_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Designation details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "Failed to update Designation details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        designation = get_object_or_404(Designation, pk=pk)
        designation.delete()
        return Response({
            "status": True,
            "message": "Designation deleted successfully."
        }, status=status.HTTP_200_OK)
    
class PriorityMasterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        priority = request.data.get("priority")
        description = request.data.get("description")

        if not priority or not description:
            return Response({
                "status": False,
                "message": "Priority and description are required.",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "priority": priority,
            "description": description,
        }

        serializer = PriorityMasterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Priority details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": False,
            "message": "Failed to add Priority details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None):
        if pk:
            priority = get_object_or_404(PriorityMaster, pk=pk)
            serializer = PriorityMasterSerializer(priority)
            data = serializer.data
        else:
            priority = PriorityMaster.objects.all()
            serializer = PriorityMasterSerializer(priority, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, pk=None):
        if pk is None:
            return Response({
                "status": False,
                "message": "Priority ID is required.",
                "data": {}
            }, status=status.HTTP_400_BAD_REQUEST)
        priority_instance = get_object_or_404(PriorityMaster, pk=pk)
        priority = request.data.get("priority", priority_instance.priority)
        description = request.data.get("description", priority_instance.description)

        data = {
            "priority": priority,
            "description": description,
        }

        serializer = PriorityMasterSerializer(priority_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Priority details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": False,
            "message": "Failed to update Priority details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        priority = get_object_or_404(PriorityMaster, pk=pk)
        priority.delete()
        return Response({
            "status": True,
            "message": "Priority deleted successfully."
        }, status=status.HTTP_200_OK)
 
class TaskCreation(APIView):

    def post(self, request):
        try:
            stake_holder = request.data.get("stake_holder", [])
            if isinstance(stake_holder, str):
                stake_holder = json.loads(stake_holder)
        except json.JSONDecodeError:
            return Response({
                "status": False,
                "message": "Invalid JSON format in stake_holder.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "project": request.data.get("project_id"),
            "task_title": request.data.get("task_title"),
            "task_describtion": request.data.get("task_describtion"),
            "teams": request.data.get("teams_id"),
            "Assignee": request.data.get("Assignee_id"),
            "task_creater": request.data.get("task_creater_id"),
            "stake_holder": stake_holder,
            "start_date": request.data.get("start_date"),
            "end_date": request.data.get("end_date"),
            "assigned_hours": request.data.get("assigned_hours"),
            "priority_level": request.data.get("priority_level"),
            "milestone": request.data.get("milestone"),
            "sprint": request.data.get("sprint"),
            "module": request.data.get("module"),
            "attachment": request.data.get("attachment"),
        }

        serializer = TaskDetailsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Task details added successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": False,
            "message": f"Failed to add Task details: {serializer.errors}"
        }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        if pk:
            task = get_object_or_404(TaskDetails, pk=pk)
            serializer = TaskDetailsSerializer(task)
            data = serializer.data
        else:
            task = TaskDetails.objects.all()
            serializer = TaskDetailsSerializer(task, many=True)
            data = serializer.data

        return Response({
            "status": True,
            "data": data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        task = get_object_or_404(TaskDetails, pk=pk)

        try:
            stake_holder = request.data.get("stake_holder", task.stake_holder)
            if isinstance(stake_holder, str):
                stake_holder = json.loads(stake_holder)
        except json.JSONDecodeError:
            return Response({
                "status": False,
                "message": "Invalid JSON format in stake_holder.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "project": request.data.get("project_id", task.project.id if task.project else None),
            "task_title": request.data.get("task_title", task.task_title),
            "task_describtion": request.data.get("task_describtion", task.task_describtion),
            "teams": request.data.get("teams", task.teams.id if task.teams else None),
            "Assignee": request.data.get("Assignee", task.Assignee.id if task.Assignee else None),
            "task_creater": request.data.get("task_creater", task.task_creater.id if task.task_creater else None),
            "stake_holder": stake_holder,
            "start_date": request.data.get("start_date", task.start_date),
            "end_date": request.data.get("end_date", task.end_date),
            "assigned_hours": request.data.get("assigned_hours", task.assigned_hours),
            "priority_level": request.data.get("priority_level", task.priority_level),
            "milestone": request.data.get("milestone", task.milestone),
            "sprint": request.data.get("sprint", task.sprint),
            "module": request.data.get("module", task.module),
            "attachment": request.data.get("attachment", task.attachment),
        }

        serializer = TaskDetailsSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Task details updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": False,
            "message": "Failed to update Task details",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(TaskDetails, pk=pk)
        task.delete()
        return Response({
            "status": True,
            "message": "Task deleted successfully."
        }, status=status.HTTP_200_OK)
    
class TaskBulkUpdate(APIView):
    def post(self, request):
        tasks_data = request.data.get("tasks")

        if not isinstance(tasks_data, list):
            return Response({
                "status": False,
                "message": "'tasks' must be a list (even if only one task)."
            }, status=status.HTTP_400_BAD_REQUEST)

        updated_tasks = []
        errors = []

        for task_data in tasks_data:
            task_id = task_data.get("id")
            if not task_id:
                errors.append({"error": "Missing 'id'", "data": task_data})
                continue

            try:
                task_instance = TaskDetails.objects.get(id=task_id)
            except TaskDetails.DoesNotExist:
                errors.append({"error": f"Task with id {task_id} not found"})
                continue

            serializer = TaskDetailsSerializer(task_instance, data=task_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_tasks.append(serializer.data)
            else:
                errors.append({"id": task_id, "error": serializer.errors})

        if errors:
            return Response({
                "status": False,
                "message": "Partial update completed with errors",
                "updated_tasks": updated_tasks,
                "errors": errors
            }, status=status.HTTP_207_MULTI_STATUS)

        return Response({
            "status": True,
            "message": "Tasks updated successfully",
            "updated_tasks": updated_tasks
        }, status=status.HTTP_200_OK)
    
class TaskAccept(APIView):
    def post(self, request, pk):
        task = get_object_or_404(TaskDetails, pk=pk)

        data = {
            "actual_start_date": timezone.now().date(),
            "status": "Started"  
        }

        serializer = TaskDetailsSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Task accepted and started",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Failed to update task",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class TaskHold(APIView):
    def post(self, request, pk):
        task = get_object_or_404(TaskDetails, pk=pk)

        data = {
            "status": "Hold"  
        }

        serializer = TaskDetailsSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Task Hold",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Failed to Hold task",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class TaskFinish(APIView):
    def post(self, request, pk):
        task = get_object_or_404(TaskDetails, pk=pk)


        data = {
            "actual_hours": request.data.get("actual_hours"),
            "actual_end_date": timezone.now().date(),
            "status": "Completed"  
        }

        serializer = TaskDetailsSerializer(task, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": True,
                "message": "Task marked as finished",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "status": False,
                "message": "Failed to update task",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
class AllUsersWithTeam(APIView):
    def get(self, request):
        users = User.objects.select_related("team").all()

        user_data = []
        for user in users:
            user_data.append({
                "id": user.id,
                "employee_name": user.employee_name,
                "team_name": user.team.team_name if user.team else None
            })

        return Response({
            "status": True,
            "message": "User list with team names",
            "data": user_data
        }, status=status.HTTP_200_OK)


class AllocatedEmployeesByTeam(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team_name = request.data.get("team_name") 

        if not team_name:
            return Response({
                "status": False,
                "message": "Please provide a team name using ?team=team_name"
            }, status=400)

        allocated_employees = []

        # Loop through all projects
        for project in Project.objects.exclude(resource_allocation=None):
            try:
                allocation_list = project.resource_allocation
                if isinstance(allocation_list, str):
                    allocation_list = json.loads(allocation_list)
                for emp in allocation_list:
                    if emp.get("team", "").lower() == team_name.lower():
                        emp_info = {
                            "id": emp.get("id"),
                            "employee_name": emp.get("employee_name")
                        }
                        if emp_info not in allocated_employees:
                            allocated_employees.append(emp_info)
            except Exception as e:
                continue

        return Response({
            "status": True,
            "team": team_name,
            "employees": allocated_employees
        }, status=200)

class AllocatedResourceView(APIView):
    def post(self, request):
        project_id = request.data.get("project_id")
        if not project_id:
            return Response({
                "status": False,
                "message": "project_id is required.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        project = get_object_or_404(Project, pk=project_id)
        resource_allocation = project.resource_allocation or []

        # Parse JSON string if needed
        if isinstance(resource_allocation, str):
            try:
                resource_allocation = json.loads(resource_allocation)
            except json.JSONDecodeError:
                resource_allocation = []

        team_set = set()
        filtered_resources = []

        for resource in resource_allocation:
            team = resource.get("team")
            if team:
                team_set.add(team.lower())  # normalize case
            filtered_resources.append({
                "id": resource.get("id"),
                "team": team,
                "employee_name": resource.get("employee_name")
            })

        return Response({
            "status": True,
            "message": "Allocated resource data fetched successfully.",
            "data": filtered_resources,
            "team": list(team_set)
        }, status=status.HTTP_200_OK)
    
class AllProjectsSummaryAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        project_data = []

        for project in projects:
            # Calculate days left
            days_left = (project.end_date - date.today()).days if project.end_date else None

            # Task completion
            total_tasks = TaskDetails.objects.filter(project=project).count()
            completed_tasks = TaskDetails.objects.filter(project=project, status__iexact="complete").count()
            completion_percent = round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0

            # Get manager info using manager_id directly
            manager = User.objects.filter(id=project.manager_id).first()
            manager_name = manager.employee_name if manager else None
            manager_image = request.build_absolute_uri(manager.profile_image.url) if manager and manager.profile_image else None

            # Append project info
            project_data.append({
                "project_id": project.id,
                "project_code": project.project_code,
                "project_name": project.project_name,
                "description": project.description,
                "manager": manager_name,
                "manager_profile": manager_image,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "milestone": project.milestone,
                "budget": project.budget,
                "resource_allocation": project.resource_allocation,
                "days_left": days_left,
                "completion_percent": completion_percent,
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
            })

        return Response(project_data, status=status.HTTP_200_OK)
class AllocatedStakeHolder(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({
                "status": False,
                "message": "user_id is required.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        tasks = TaskDetails.objects.all()
        tasks_data = TaskDetailsSerializer(tasks, many=True).data

        stake_holder_tasks = []
        for task in tasks_data:
            if task.get("stake_holder"):
                for stake_holder in task["stake_holder"]:
                    print(stake_holder)
                    if stake_holder.get("user_id") == int(user_id):
                        stake_holder_tasks.append(task)
                        break
        

        return Response({
            "status": True,
            "message": "Stakeholder task fetched!.",
            "data": stake_holder_tasks,
        }, status=status.HTTP_200_OK)
    
class EmployeeAssignedTask(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({
                "status": False,
                "message": "user_id is required.",
                "data": []
            }, status=status.HTTP_400_BAD_REQUEST)

        tasks = TaskDetails.objects.filter(Assignee=user_id)
        tasks_data = TaskDetailsSerializer(tasks, many=True).data

        return Response({
            "status": True,
            "message": "Assigned task fetched!.",
            "data": tasks_data,
        }, status=status.HTTP_200_OK)
 
class GroupedTaskView(APIView):
    def get(self, request, project_id):
        tasks = TaskDetails.objects.filter(project_id=project_id).exclude(milestone=None).exclude(sprint=None)

        data_structure = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for task in tasks:
            milestone_key = f"milestone {task.milestone}"
            sprint_key = f"sprint {task.sprint}"
            module_key = task.module

            duration = (
                (task.end_date - task.start_date).days
                if task.start_date and task.end_date else 0
            )

            data_structure[milestone_key][sprint_key][module_key].append({
                "tasktile": task.task_title,
                "duartion": str(duration),
                "status": task.status,
                "assigned_hours": task.assigned_hours or 0,
                "actual_hours": task.actual_hours or 0,
                "assignee_name": task.Assignee.employee_name if task.Assignee else "Unassigned"
            })


        response_data = []
        for milestone, sprints in data_structure.items():
            sprint_list = []
            for sprint, modules in sprints.items():
                module_list = []
                for module, task_list in modules.items():
                    module_list.append({
                        "modulename": module,
                        "tasknames": task_list
                    })
                sprint_list.append({
                    "sprints": sprint,
                    "tasknames": module_list
                })
            response_data.append({
                "milestone": milestone,
                "sprints": sprint_list
            })

        serializer = MilestoneSerializer(response_data, many=True)
        return Response(serializer.data)