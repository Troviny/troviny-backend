from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken

# Get the User model
User = get_user_model()

# Generate JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password", format="password"),
            "phone_number": openapi.Schema(type=openapi.TYPE_STRING, description="Phone Number"),
            "address": openapi.Schema(type=openapi.TYPE_STRING, description="Address"),
            "profile_picture": openapi.Schema(type=openapi.TYPE_STRING, description="Profile Picture URL"),
            "country": openapi.Schema(type=openapi.TYPE_STRING, description="Country"),
            "city": openapi.Schema(type=openapi.TYPE_STRING, description="City"),
            "role": openapi.Schema(type=openapi.TYPE_STRING, description="User Role"),
        },
        required=["username", "email", "password"],
    ),
    responses={201: "User registered successfully", 400: "Username or Email already taken"},
    tags=["Auth"],
)
@api_view(["POST"])
def register(request):
    """User Registration"""
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    phone_number = request.data.get("phone_number", "")
    address = request.data.get("address", "")
    profile_picture = request.data.get("profile_picture", "")
    country = request.data.get("country", "")
    city = request.data.get("city", "")
    role = request.data.get("role", "")

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username is already taken."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "A user with this email already exists."}, status=400)

    user = User.objects.create(
        username=username,
        email=email,
        phone_number=phone_number,
        address=address,
        profile_picture=profile_picture,
        country=country,
        city=city,
        role=role,
        password=make_password(password),  # Hash password before saving
    )

    tokens = get_tokens_for_user(user)
    return Response({"user_id": user.id, "tokens": tokens}, status=201)

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="Password", format="password"),
        },
        required=["username", "password"],
    ),
    responses={200: "Login Successful", 400: "Invalid Credentials"},
    tags=["Auth"],
)
@api_view(["POST"])
def login(request):
    """User Login"""
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({"error": "Invalid username or password."}, status=400)

    if not user.is_active:
        return Response({"error": "This account is inactive. Contact support."}, status=400)

    tokens = get_tokens_for_user(user)
    return Response({"user_id": user.id, "tokens": tokens}, status=200)

@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "refresh_token": openapi.Schema(type=openapi.TYPE_STRING, description="Refresh token to blacklist"),
        },
        required=["refresh_token"],
    ),
    responses={200: "Logged out successfully", 400: "Invalid token"},
    tags=["Auth"],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    """User Logout"""
    refresh_token = request.data.get("refresh_token")
    access_token = request.headers.get("Authorization", "").split(" ")[1]  # Extract access token

    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=400)

    try:
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()

        # Blacklist the access token
        BlacklistedToken.objects.create(token=access_token)

        return Response({"message": "Logged out successfully"}, status=200)
    except Exception:
        return Response({"error": "Invalid or expired refresh token"}, status=400)

@swagger_auto_schema(
    method="get",
    responses={200: "User profile"},
    tags=["User"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    """Get the authenticated user's profile"""
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address,
        "profile_picture": user.profile_picture,
        "country": user.country,
        "city": user.city,
        "role": user.role,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
    }, status=200)

@swagger_auto_schema(
    method="get",
    manual_parameters=[
        openapi.Parameter(
            "user_id",
            openapi.IN_PATH,
            description="ID of the user to retrieve",
            type=openapi.TYPE_INTEGER,
        )
    ],
    responses={200: "User profile", 404: "User not found"},
    tags=["User"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_single_user_profile(request, user_id=None):
    """Retrieve a single user profile"""
    try:
        user = User.objects.get(id=user_id) if user_id else request.user
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone_number": user.phone_number,
        "address": user.address,
        "profile_picture": user.profile_picture,
        "country": user.country,
        "city": user.city,
        "role": user.role,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
    }, status=200)

@swagger_auto_schema(
    method="get",
    responses={200: "List of users"},
    tags=["User"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """Retrieve all users"""
    users = User.objects.all().values(
        "id", "username", "email", "phone_number", "address",
        "profile_picture", "country", "city", "role", "is_active", "is_staff"
    )
    return Response(list(users), status=200)
