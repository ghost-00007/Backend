from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.timezone import now
from django.conf import settings

from identity.models import Roles



class Department(models.Model):
    department_code = models.CharField(max_length=25, blank=True, null=False, unique=True)
    department_name = models.CharField(max_length=25, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "department_details"

class Project(models.Model):
    project_code = models.CharField(max_length=25, blank=True, null=False, unique=True)
    project_name = models.CharField(max_length=25, blank=True, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    milestone = models.IntegerField(blank=True, null=False)
    budget = models.IntegerField(blank=True, null=False)
    resource_allocation = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "project_details"

class Designation(models.Model):
    department= models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    designation = models.CharField(max_length=150, blank=True, null=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "designation_details"


class Teams(models.Model):
    team_name = models.CharField(max_length=25, blank=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "team_details"




class PriorityMaster(models.Model):
    priority = models.CharField(max_length=25, blank=True, null=False, unique=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    lastUpdate = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "priority_master_details"
        
class TaskDetails(models.Model):
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    task_title = models.CharField(max_length=25, blank=True)
    task_describtion = models.CharField(max_length=250, blank=True)
    
    teams = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True)
    
    Assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    task_creater = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tasks'
    )
    stake_holder = models.JSONField(blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    actual_end_date = models.DateField(null=True, blank=True)

    assigned_hours = models.IntegerField(default=0,null=True)
    actual_hours = models.IntegerField(default=0,null=True)

    status = models.CharField(max_length=25, blank=True, default='Not Started')

    priority_level = models.CharField(max_length=25, blank=True)
    milestone = models.IntegerField(blank=True, null=True)
    sprint = models.IntegerField(blank=True, null=True)
    module = models.CharField(max_length=25, blank=True)

    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)

    def __str__(self):
        return self.task_title
    
    class Meta:
        db_table = "task_details"



    


