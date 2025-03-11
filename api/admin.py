from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# Define an inline admin descriptor for UserProfile model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "Additional Info"
    fk_name = "user"

# Extend the default UserAdmin to include UserProfile fields
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        return []

# Unregister default User model and register it with the modified admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
