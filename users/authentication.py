from django.contrib.auth.backends import BaseBackend
from .models import User
from django.contrib.auth.hashers import make_password, check_password

class AuthBackend(BaseBackend):
    """
    Custom authentication backend to authenticate users using email and password.
    """
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None