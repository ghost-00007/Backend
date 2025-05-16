from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from tokenize import TokenError
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode

from .authentication import AuthBackend
from .serializers import UserSerializer,UserMinimalSerializer,PasswordResetConfirmSerializer

from identity.models import RolePermission
from identity.serializers import RolePermissionSerializer

class UserLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = AuthBackend().authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            serialized_user = UserSerializer(user)

            if user.is_superuser:
                access = RolePermission.objects.all()
                accessSerializerData = RolePermissionSerializer(access, many=True).data
                return Response({
                    'status': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serialized_user.data,
                    'role_permission': accessSerializerData,
                }, status=200)
            else:
                userRole = serialized_user.data['role']['id']
                access = RolePermission.objects.filter(role=userRole)
                accessSerializerData = RolePermissionSerializer(access, many=True).data

                return Response({
                    'status': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serialized_user.data,
                    'role_permission': accessSerializerData,
                }, status=200)
        else:   
            return Response({"message": "Invalid credentials"}, status=401)

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"status": True, "message": "Logout successful."}, status=205)
        except KeyError:
            return Response({"status": False, "message": "Refresh token is required."}, status=400)
        except TokenError as e:
            return Response({"status": False, "message": str(e)}, status=400)

User = get_user_model()

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        new_password = request.data.get("new_password")

        if not new_password:
            return Response({"error": "New password is required."}, status=400)

        user = request.user
        user.set_password(new_password)
        user.save()

        return Response({"message": f"Password reset successful for {user.email}."}, status=200)

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk:
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(user)
            return Response({
                "status":True,
                "message": "User details fetched!",
                "data": serializer.data,
            },status=status.HTTP_200_OK,
            )
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({
                "status":True,
                "message": "User details fetched!",
                "data": serializer.data,
            },status=status.HTTP_200_OK,
            )

    def post(self, request):
        data = {
        'email': request.data.get('email'),
        'role_id': request.data.get('role_id'),
        'employee_name': request.data.get('employee_name'),
        'employee_code': request.data.get('employee_code'),
        'department_id': request.data.get('department_id'),
        'designation_id': request.data.get('designation_id'),
        'reporting_manager_id': request.data.get('reporting_manager_id'),
        'team_id': request.data.get('team_id'),
        'profile_image': request.data.get('profile_image'),
    }


        userSerializer = UserSerializer(data=data)
        if userSerializer.is_valid():
            userSerializer.save()
            currentUser = User.objects.get(email=request.data.get('email'))
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(currentUser)
            uid = urlsafe_base64_encode(force_bytes(currentUser.pk))

            set_link = f"{settings.FRONTEND_URL}/setPassword/{uid}/{token}/"

            subject = "Set Password Request"

            html_message = render_to_string(
                "Email_HTML/set_password.html",
                {
                    "user": currentUser,
                    "reset_link": set_link,
                    "role": f"{currentUser.role} {currentUser.designation.designation}",
                },
            )
            plain_message = strip_tags(html_message)
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [request.data.get('email')],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                return Response(
                    {"error": "Failed to send email. Please try again later."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            return Response(
                {
                    'status': True,
                    'message': 'Employee added successfully!',
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': False,
                    'message': userSerializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        data = {
                'email': request.data.get('email'),
                'role_id': request.data.get('role_id'),
                'employee_name': request.data.get('employee_name'),
                'employee_code': request.data.get('employee_code'),
                'department_id': request.data.get('department_id'),
                'designation_id': request.data.get('designation_id'),
                'reporting_manager_id': request.data.get('reporting_manager_id'),
                'team_id': request.data.get('team_id'),
                'profile_image': request.data.get('profile_image'),
                }
        

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'status': True, 'message': 'Employee updated successfully!'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'status': False, 'message': 'Update failed!', 'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(
            {
                'status': True, 
                'message': 'Employee deleted successfully!',
            },
            status=status.HTTP_200_OK
        )

class UserEmailConfirmation(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            currentUser = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {
                    'status': False,
                    'message': 'No User Details Found!',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(currentUser)
        uid = urlsafe_base64_encode(force_bytes(currentUser.pk))

        set_link = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"

        subject = "Reset Password Request"

        html_message = render_to_string(
            "Email_HTML/reset_password.html",
            {
                "user": currentUser,
                "reset_link": set_link,
                "role": currentUser.role
            },
        )
        plain_message = strip_tags(html_message)
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {"error": "Failed to send email. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                'status': True,
                'message': 'Reset link sent successfully!',
            },
            status=status.HTTP_201_CREATED
        )
        
class UserTeamListAPIView(APIView):
    def get(self, request):
        users = User.objects.select_related('team').all()
        serializer = UserMinimalSerializer(users, many=True)
        return Response({"status": True, "data": serializer.data}, status=status.HTTP_200_OK)
    

class password_reset_confirm(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']

            UserModel = get_user_model()
            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = UserModel.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None

            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(password)
                user.save()
                return Response({
                    "status": True,
                    "detail": "Password has been reset."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "status": False,
                    "detail": "Invalid token or user ID."
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "status": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
