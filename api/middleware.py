import traceback, time
from django.http import JsonResponse, Http404
from django.core.exceptions import (
    PermissionDenied,
    SuspiciousOperation,
    ValidationError as DjangoValidationError,
)
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.cache import cache


class CustomExceptionMiddleware:
    """
    Middleware to catch exceptions and return JSON error responses with proper status codes.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as exc:
            traceback.print_exc()
            if isinstance(exc, Http404):
                status_code = 404
                message = "Not Found"
            elif isinstance(exc, PermissionDenied):
                status_code = 403
                message = "Permission Denied"
            elif isinstance(exc, (DRFValidationError, DjangoValidationError)):
                status_code = 400
                message = getattr(exc, "detail", str(exc))
            elif isinstance(exc, SuspiciousOperation):
                status_code = 400
                message = "Bad Request"
            else:
                status_code = 500
                message = "Internal Server Error"

            return JsonResponse(
                {"detail": message, "error": str(exc)}, status=status_code
            )


class RateLimitMiddleware:
    """
    Middleware to enforce rate limiting.
    Limits each client to a fixed number of requests per time window.
    Uses Redis (via Django's cache) for tracking.
    """

    RATE_LIMIT = 100
    WINDOW_SIZE = 60

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        identifier = self.get_identifier(request)
        if identifier:
            current_window = int(time.time() // self.WINDOW_SIZE)
            key = f"rl:{identifier}:{current_window}"
            try:
                count = cache.incr(key)
            except ValueError:
                cache.add(key, 1, self.WINDOW_SIZE)
                count = 1

            if count > self.RATE_LIMIT:
                return JsonResponse(
                    {"detail": "Too many requests, rate limit exceeded."}, status=429
                )
        response = self.get_response(request)
        return response

    def get_identifier(self, request):
        """
        Returns a string identifier for the client.
        If the user is authenticated, use the user ID.
        Otherwise, use the client's IP address.
        """
        if hasattr(request, "user") and request.user.is_authenticated:
            return f"user:{request.user.id}"
        else:
            ip = request.META.get("REMOTE_ADDR")
            return f"ip:{ip}" if ip else None
