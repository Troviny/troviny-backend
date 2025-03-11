from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from . import views  # Import views from the same app

# Swagger API Documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Troviny API Documentation",
        default_version='v1',
        description="API documentation for Troviny project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="bodyessam223@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

auth_urls = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('refreshToken/', TokenRefreshView.as_view(), name='token-refresh'),
]

user_urls = [
    path('user/', views.get_current_user_profile, name='get-user'),
    path('user/single_profile/<int:user_id>/', views.get_single_user_profile, name='specific-user-profile'),
    path('user/all_users', views.get_all_users, name='get-all-users'),
]

urlpatterns = [
    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    # Authentication URLs under 'auth/'
    path('auth/', include((auth_urls, 'auth'))),  

    # User URLs under 'user/'
    path('user/', include((user_urls, 'user'))),  
]
