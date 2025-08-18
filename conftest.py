import os
import django
from rest_framework.test import APIClient
import pytest

# Set the default Django settings module
# This ensures Django knows which settings to use before any tests run
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UrlShortener.settings")

# Setup Django
# Required to initialize Django for standalone test files or fixtures
django.setup()

# Fixture to provide a DRF APIClient instance to tests
# This allows making requests to the API endpoints in tests
@pytest.fixture
def api_client():
    return APIClient()
