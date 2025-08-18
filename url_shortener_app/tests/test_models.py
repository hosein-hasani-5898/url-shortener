import pytest
from django.utils import timezone
from url_shortener_app.models import ShortURL


@pytest.mark.django_db
def test_is_expired_true():
    """
    Test that `is_expired()` returns True for a URL whose expiration date is in the past.
    """
    url = ShortURL.objects.create(
        original_url="https://example.com",
        expiration=timezone.now() - timezone.timedelta(days=1)
    )
    assert url.is_expired() is True


@pytest.mark.django_db
def test_is_expired_false():
    """
    Test that `is_expired()` returns False for a URL whose expiration date is in the future.
    """
    url = ShortURL.objects.create(
        original_url="https://example.com",
        expiration=timezone.now() + timezone.timedelta(days=1)
    )
    assert url.is_expired() is False


@pytest.mark.django_db
def test_password_set_and_check():
    """
    Test setting a password and verifying correct and incorrect password checks.
    """
    url = ShortURL.objects.create(original_url="https://example.com")
    url.set_password("secret123")
    url.save()
    assert url.check_password("secret123") is True
    assert url.check_password("wrongpass") is False
