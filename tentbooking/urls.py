"""
URL configuration for tentbooking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .health import HealthCheckView

# Swagger/OpenAPI schema configuration
schema_view = get_schema_view(
   openapi.Info(
      title="🏕️ Tent Booking API",
      default_version='v1',
      description="""
      A comprehensive API for tent booking system with role-based access control.
      
      ## Features
      - User registration and authentication with JWT
      - Role-based access (Admin/Customer)
      - Tent type management
      - Booking creation and management
      - Admin dashboard for booking confirmation
      
      ## Authentication
      Use the `/api/auth/login/` or `/api/auth/token/` endpoint to get your JWT token.
      Then include it in the Authorization header as: `Bearer <your_token>`
      
      ## Roles
      - **Customer**: Can create bookings, view own bookings
      - **Admin**: Can view all bookings, confirm bookings, manage tent types
      """,
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@tentbooking.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('users.urls')),
    path('api/', include('bookings.urls')),
    
    # Swagger/OpenAPI documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
