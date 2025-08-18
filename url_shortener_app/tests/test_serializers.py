import pytest
from rest_framework.test import APIRequestFactory
from url_shortener_app.api.serializers import ShortURLSerializer
from url_shortener_app.models import ShortURL


@pytest.mark.django_db
def test_serializer_short_url_generation():
    """
    Test that ShortURLSerializer correctly generates short_code and short_url fields.
    """
    url = ShortURL.objects.create(original_url="https://example.com")
    
    # Create a fake GET request for serializer context
    factory = APIRequestFactory()
    request = factory.get('/')
    
    serializer = ShortURLSerializer(url, context={"request": request})
    data = serializer.data
    
    assert "short_code" in data
    assert "short_url" in data
    assert data["short_url"].endswith(data["short_code"])
