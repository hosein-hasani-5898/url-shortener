import pytest
from django.urls import reverse
from url_shortener_app.models import ShortURL
from django.utils import timezone
from url_shortener_app.api.utils import encode_id


@pytest.mark.django_db
def test_create_short_url(api_client):
    """
    Test creating a new short URL via API endpoint.
    """
    response = api_client.post(reverse("api-shorten"), {
        "original_url": "https://example.com"
    }, format="json")
    
    assert response.status_code == 201
    assert "short_url" in response.data


@pytest.mark.django_db
def test_redirect_short_url(api_client):
    """
    Test that accessing a short URL redirects to the original URL.
    """
    obj = ShortURL.objects.create(original_url="https://example.com")
    code = api_client.get(reverse("redirect-short", args=[encode_id(obj.id)])).status_code
    assert code in (302, 307)  # HTTP redirect codes


@pytest.mark.django_db
def test_expired_link(api_client):
    """
    Test that accessing an expired short URL returns 410 Gone.
    """
    obj = ShortURL.objects.create(
        original_url="https://example.com",
        expiration=timezone.now() - timezone.timedelta(days=1)
    )
    response = api_client.get(reverse("redirect-short", args=[encode_id(obj.id)]))
    assert response.status_code == 410


@pytest.mark.django_db
def test_password_protected(api_client):
    """
    Test behavior of password-protected short URLs:
    - Without password
    - With incorrect password
    - With correct password
    """
    obj = ShortURL.objects.create(original_url="https://example.com")
    obj.set_password("secret")
    obj.save()

    # Access without password should return 401
    response = api_client.get(reverse("redirect-short", args=[encode_id(obj.id)]))
    assert response.status_code == 401

    # Access with wrong password should return 403
    response = api_client.post(reverse("redirect-short", args=[encode_id(obj.id)]), {"password": "wrong"})
    assert response.status_code == 403

    # Access with correct password should redirect (302/307)
    response = api_client.post(reverse("redirect-short", args=[encode_id(obj.id)]), {"password": "secret"})
    assert response.status_code in (302, 307)
