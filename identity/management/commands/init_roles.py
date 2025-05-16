from django.core.management.base import BaseCommand
from django.utils.timezone import now
from identity.models import AppDetails, ModuleDetails, ComponentDetails, Roles, RolePermission


class Command(BaseCommand):
    help = 'Initialize App, Modules, Components, and Super Admin permissions'

    def handle(self, *args, **kwargs):
        # 1. Create App
        app_obj, _ = AppDetails.objects.get_or_create(
            app_name='Project Management',
            defaults={
                'domain': 'https://admin.example.com',
                'version': '1.0.0',
                'release_date': now().date(),
                'release_note': 'Initial release of Project Management'
            }
        )
        self.stdout.write(self.style.SUCCESS(f"✅ App: {app_obj.id} - {app_obj.app_name}"))

        # 2. Define Modules and Components
        module_component_map = {
            'Role': ['Role Add', 'Role Edit', 'Role View', 'Role Delete'],
            'Team': ['Team Add', 'Team Edit', 'Team View', 'Team Delete'],
            'Employee Master': ['Employee Add', 'Employee Edit', 'Employee View', 'Employee Delete'],
            'Project Master': ['Project Add', 'Project Edit', 'Project View', 'Project Delete'],
            'Department Master': ['Department Add', 'Department Edit', 'Department View', 'Department Delete'],
            'Designation Master': ['Designation Add', 'Designation Edit', 'Designation View', 'Designation Delete'],
            'Task Master': ['Task Add', 'Task Edit', 'Task View', 'Task Delete'],
            'Task Board': ['Task Drag & Drop'],
            'Stack Holder': ['View'],
            'Task List': ['View'],
            'Role Permission': ['Manage']
        }

        # 3. Create Modules and Components
        all_components = []
        for module_name, comp_list in module_component_map.items():
            module_obj, _ = ModuleDetails.objects.get_or_create(module_name=module_name, app=app_obj)
            self.stdout.write(self.style.SUCCESS(f"  ↪ Module: {module_obj.id} - {module_obj.module_name}"))

            for comp_name in comp_list:
                comp_obj, created = ComponentDetails.objects.get_or_create(
                    component_name=comp_name,
                    module=module_obj,
                    app=app_obj
                )
                all_components.append(comp_obj)
                if created:
                    self.stdout.write(self.style.SUCCESS(f"    ↪ Component Created: {comp_obj.component_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"    ↪ Component Exists: {comp_obj.component_name}"))

        # 4. Create Super Admin role
        role_obj, _ = Roles.objects.get_or_create(role='Super Admin', defaults={'description': 'Has all access'})
        self.stdout.write(self.style.SUCCESS(f"✅ Role: {role_obj.id} - {role_obj.role}"))

        # 5. Assign permissions
        created_count = 0
        for comp in all_components:
            if not RolePermission.objects.filter(role=role_obj, component=comp).exists():
                RolePermission.objects.create(
                    role=role_obj,
                    app=comp.app,
                    module=comp.module,
                    component=comp,
                    can_access=True
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"      → Permission Added: {comp.component_name}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Done. Total new permissions created: {created_count}"))
