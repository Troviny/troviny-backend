from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from api.models import UserProfile

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ["user", "phone_number", "address", "profile_picture", "country", "city", "role"]

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    email = serializers.EmailField(required=True)

    # Additional UserProfile fields
    phone_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    profile_picture = serializers.CharField(required=False, allow_blank=True)
    country = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    role = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "first_name", "last_name",
                  "phone_number", "address", "profile_picture", "country", "city", "role"]

    def validate_email(self, value):
        """Ensure email is unique"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """Create user and associate with UserProfile"""
        profile_data = {
            "phone_number": validated_data.pop("phone_number", None),
            "address": validated_data.pop("address", None),
            "profile_picture": validated_data.pop("profile_picture", None),
            "country": validated_data.pop("country", None),
            "city": validated_data.pop("city", None),
            "role": validated_data.pop("role", None),
        }

        # Create the User
        user = User.objects.create_user(**validated_data)

        # Create the UserProfile and associate with the user
        UserProfile.objects.create(user=user, **profile_data)

        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Check if user exists
        user = User.objects.filter(email=email).first()
        if user is None:
            raise serializers.ValidationError("User not found. Please register.")

        # Authenticate using email instead of username
        user = authenticate(username=user.email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials. Please try again.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive. Contact support.")

        data["user"] = user
        return data
