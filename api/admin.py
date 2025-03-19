from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserModel  # Ensure this matches your actual import path

# Extend the default UserAdmin to include custom fields
class CustomUserAdmin(UserAdmin):
    model = UserModel

    # Display these fields in the admin panel list view
    list_display = ("id", "username", "email", "phone_number", "role", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff", "role", "country", "city")

    # Define fieldsets for adding/editing users in the admin panel
    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal Information", {"fields": ("phone_number", "address", "profile_picture", "country", "city", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "updated_on")}),
    )

    # Define fields displayed when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "phone_number", "role", "is_active", "is_staff"),
        }),
    )

    search_fields = ("username", "email", "phone_number")
    ordering = ("id",)

# Register the new UserModel with custom admin settings
admin.site.register(UserModel, CustomUserAdmin)
