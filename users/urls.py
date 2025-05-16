from django.urls import path
from .views import UserLogin, PasswordResetView, UserCreateView, UserEmailConfirmation,UserTeamListAPIView, UserLogout,password_reset_confirm

urlpatterns = [
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
    path('reset_password/', PasswordResetView.as_view(), name='password-reset'),
    path('create_user/', UserCreateView.as_view(), name='create-user'),
    path('create_user/<int:pk>/', UserCreateView.as_view(), name='get-user-by-id'),
    path('verify_email/', UserEmailConfirmation.as_view(), name='verify-email'),

    path('teamusers/', UserTeamListAPIView.as_view(), name='user-team-info'),
    path('password-reset-confirm/', password_reset_confirm.as_view(), name='password_reset_confirm'),

    # path('api/token/', include('rest_framework_simplejwt.urls')),
]