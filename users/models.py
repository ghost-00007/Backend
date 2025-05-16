# users/models.py

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from project_management.models import Department,Designation,Teams
from identity.models import Roles


class UserManager(BaseUserManager):
    """
    Custom manager for the User model to support email-based authentication.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('employee_name', 'SUPER-USER')

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)

    # class Role(models.TextChoices):
    #     SUPERUSER = 'SUPERUSER', 'Super User'
    #     ADMIN = 'ADMIN', 'Admin'
    #     SUPPORT = 'SUPPORT', 'Support Manager'
    #     EMPLOYEE = 'EMPLOYEE', 'Employee'

    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)

    is_admin = models.BooleanField(default=False)

    employee_name = models.CharField(max_length=255)
    employee_code = models.CharField(max_length=255)
    department= models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="emp_department")
    designation= models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    reporting_manager = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    team=models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:
        db_table = 'users'
