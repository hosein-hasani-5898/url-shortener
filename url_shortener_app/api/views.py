from datetime import timedelta
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import redirect, get_object_or_404
from url_shortener_app.models import ShortURL, URLClick
from .serializers import ShortURLSerializer, ClickReportSerializer
from .utils import decode_id
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ShortURLCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for creating a new ShortURL instance.
    """
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer

    @swagger_auto_schema(
        request_body=ShortURLSerializer,
        responses={201: ShortURLSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


def get_client_ip(request):
    """
    Retrieve the client's IP address from request headers or remote address.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@swagger_auto_schema(
    method='get',
    manual_parameters=[openapi.Parameter(
        'code',
        openapi.IN_PATH,
        description="Short URL code",
        type=openapi.TYPE_STRING
    )],
    operation_description="Redirects a short URL (no password required for GET).",
    responses={
        302: 'Redirect to original URL',
        401: 'Password required',
        403: 'Invalid password',
        404: 'Invalid URL',
        410: 'Expired link'
    }
)
@swagger_auto_schema(
    method='post',
    manual_parameters=[openapi.Parameter(
        'code',
        openapi.IN_PATH,
        description="Short URL code",
        type=openapi.TYPE_STRING
    )],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for protected link')}
    ),
    operation_description="Redirects a password-protected short URL (POST must include password).",
    responses={
        302: 'Redirect to original URL',
        403: 'Invalid password',
        404: 'Invalid URL',
        410: 'Expired link'
    }
)
@api_view(['GET', 'POST'])
def redirect_short_url(request, code):
    """
    Redirect the short URL to its original URL.
    Handles password protection, expiration, and click tracking.
    """
    # Decode short code to database ID
    id = decode_id(code)
    if id is None:
        return Response({"error": "Invalid URL"}, status=404)

    obj = get_object_or_404(ShortURL, id=id)

    # Check expiration
    if obj.is_expired():
        return Response({"error": "This link has expired"}, status=410)

    # Handle password-protected links
    if obj.password:
        if request.method == 'POST':
            pw = request.data.get('password', '')
            if not obj.check_password(pw):
                return Response({"error": "Invalid password"}, status=403)
        else:
            return Response({"detail": "Password required"}, status=401)

    # Track click by unique IP
    ip = get_client_ip(request)
    URLClick.objects.get_or_create(
        url=obj,
        ip_address=ip,
        defaults={'user_agent': request.META.get('HTTP_USER_AGENT', '')}
    )
    
    # Increment total clicks and update last clicked timestamp
    obj.clicks += 1
    obj.last_clicked = timezone.now()
    obj.save(update_fields=["clicks", "last_clicked"])

    # Redirect to the original URL
    return redirect(obj.original_url)


@swagger_auto_schema(
    method='get',
    responses={200: ClickReportSerializer}
)
@api_view(['GET'])
def click_report(request):
    """
    Return click statistics: clicks today and clicks in the last week.
    """
    today = timezone.now().date()
    clicks_today = ShortURL.objects.filter(last_clicked__date=today).count()

    week_ago = timezone.now() - timedelta(days=7)
    clicks_week = ShortURL.objects.filter(last_clicked__gte=week_ago).count()

    serializer = ClickReportSerializer({
        "clicks_today": clicks_today,
        "clicks_week": clicks_week
    })
    return Response(serializer.data)
