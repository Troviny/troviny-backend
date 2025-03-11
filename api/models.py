from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now  # Import 'now' to set a default timestamp

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    role = models.TextField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
