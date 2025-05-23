from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Link to app's URLconf
    path('api/', include('project_management.urls')),  # Link to app's URLconf
    path('api/', include('identity.urls')),  # Link to app's URLconf
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
