from django.urls import path
from . import views 

urlpatterns = [
    path('department/', views.DepartmentView.as_view(), name='Department'), 
    path('department/<int:pk>/', views.DepartmentView.as_view(), name='Department'),

    path('project/', views.ProjectView.as_view(), name='Project'), 
    path('project/<int:pk>/', views.ProjectView.as_view(), name='Project'),

    path('teams/', views.TeamsView.as_view(), name='Teams'), 
    path('teams/<int:pk>/', views.TeamsView.as_view(), name='Teams'),

    path('designation/', views.DesignationView.as_view(), name='Designation-View'), 
    path('designation/<int:pk>/', views.DesignationView.as_view(), name='Designation-View'),

    path('priority/', views.PriorityMasterView.as_view(), name='PriorityMaster'),
    path('priority/<int:pk>/', views.PriorityMasterView.as_view(), name='PriorityMaster'),
    
    path('taskcreation/', views.TaskCreation.as_view(), name='Task-Creation'), 
    path('taskcreation/<int:pk>/', views.TaskCreation.as_view(), name='Task-Creation'),

    path('taskbulkupdate', views.TaskBulkUpdate.as_view(), name='TaskBulk-Update'),

    path('taskaccept/<int:pk>/', views.TaskAccept.as_view(), name='Task-Accept'),
    path('taskhold/<int:pk>/', views.TaskHold.as_view(), name='Task-Hold'),
    path('taskfinish/<int:pk>/', views.TaskFinish.as_view(), name='Task-Finish'),

    path("users/by-team/", views.AllUsersWithTeam.as_view(), name="users-by-team"),

    path("allocatedemployeelist/", views.AllocatedEmployeesByTeam.as_view(), name="users-by-team"),

    path("getallocatedresources/", views.AllocatedResourceView.as_view(), name="get-allocated-resources"),

    path("getStakeHolders/", views.AllocatedStakeHolder.as_view(), name="get-stake-holders"),
    path('all-projects-summary/', views.AllProjectsSummaryAPIView.as_view(), name='all-projects-summary'),

    path('getEmployeeTask/', views.EmployeeAssignedTask.as_view(), name='employee-task'),

    path('grouped-tasks/<int:project_id>/', views.GroupedTaskView.as_view(), name='grouped-tasks')


]

