from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model to return user details in API responses"""

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "address", 
                  "profile_picture", "country", "city", "role", "is_active", "is_staff"]
