from rest_framework.throttling import AnonRateThrottle


class PasswordProtectedURLThrottle(AnonRateThrottle):
    """
    Throttle class for limiting anonymous requests to password-protected URLs.
    Limits to 5 requests per minute per IP address.
    """
    rate = "5/minute"
