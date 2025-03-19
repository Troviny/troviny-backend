from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

# Get the custom User model
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
    request_body=RegisterSerializer,
    responses={201: "User registered successfully", 400: "Username or Email already taken"},
    tags=["Auth"],
)
@api_view(["POST"])
def register(request):
    """User Registration"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({"data": UserSerializer(user).data, "tokens": tokens}, status=201)
    return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method="post",
    request_body=LoginSerializer,
    responses={200: "Login Successful", 400: "Invalid Credentials"},
    tags=["Auth"],
)
@api_view(["POST"])
def login(request):
    """User Login"""
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.validated_data["user"]
        tokens = get_tokens_for_user(user)
        return Response({"user_id": user.id, "tokens": tokens}, status=200)

    return Response(serializer.errors, status=400)

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
    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=400)

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@swagger_auto_schema(
    method="get",
    responses={200: UserSerializer},
    tags=["User"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_current_user_profile(request):
    """Get the authenticated user's profile"""
    return Response(UserSerializer(request.user).data, status=200)

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
    responses={200: UserSerializer, 404: "User not found"},
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

    return Response(UserSerializer(user).data, status=200)

@swagger_auto_schema(
    method="get",
    responses={200: UserSerializer(many=True)},
    tags=["User"],
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    """Retrieve all users"""
    users = User.objects.all()
    return Response(UserSerializer(users, many=True).data, status=200)
