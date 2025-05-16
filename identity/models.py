from django.db import models

# Create your models here.
class AppDetails(models.Model):
    app_name= models.CharField(max_length=254, blank=True, null=True)
    domain= models.URLField(max_length=254, blank=True, null=True)
    version= models.CharField(max_length=25, blank=True, null=True)
    release_date= models.DateField(blank=True, null=True)
    release_note= models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    last_update= models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table= 'app_details'
 
    def __str__(self):
        return f"{self.app_name} - {self.version}"
 
# Create your models for connect App and Module
class ModuleDetails(models.Model):
    app= models.ForeignKey(AppDetails, on_delete=models.SET_NULL, null=True, blank=True)
    module_name= models.CharField(max_length=254, blank=True, null=True)
 
    class Meta:
        db_table= 'app_module_details'
 
    def __str__(self):
        return f"{self.module_name}"
 
# Create your models for Configure Component And Module
class ComponentDetails(models.Model):
    component_name= models.CharField(max_length=254, blank=True, null=True)
    module= models.ForeignKey(ModuleDetails, on_delete=models.SET_NULL, null=True, blank=True)
    app= models.ForeignKey(AppDetails, on_delete=models.SET_NULL, null=True, blank=True)
 
    class Meta:
        db_table= 'app_component_details'
 
    def __str__(self):
        return f"{self.component_name}"
class Roles(models.Model):
    role= models.CharField(max_length=254, blank=True, null= True)
    description= models.CharField(blank=True, null= True)
    created_at= models.DateTimeField(auto_now_add=True)
    last_update= models.DateTimeField(auto_now=True)
 
    class Meta:
        db_table= 'identity_roles'
 
    def __str__(self):
        return f'{self.role}'
   
class RolePermission(models.Model):
    role= models.ForeignKey(Roles, on_delete=models.CASCADE)
    app= models.ForeignKey(AppDetails, on_delete=models.CASCADE)
    module= models.ForeignKey(ModuleDetails, on_delete=models.CASCADE)
    component= models.ForeignKey(ComponentDetails, on_delete=models.CASCADE)
    can_access= models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    last_update= models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.role} - {self.component}"
   
    class Meta:
        db_table= "identity_role_permission"