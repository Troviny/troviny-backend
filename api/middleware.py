from django.http import JsonResponse
from .models import BlacklistedToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class BlacklistAccessTokenMiddleware:
    """Middleware to reject blacklisted access tokens"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                access_token = auth_header.split(" ")[1]
                if BlacklistedToken.objects.filter(token=access_token).exists():
                    return JsonResponse({"error": "Invalid token, please log in again"}, status=401)
            except IndexError:
                return JsonResponse({"error": "Invalid token format"}, status=401)

        return self.get_response(request)
