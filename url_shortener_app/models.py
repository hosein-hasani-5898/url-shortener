from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password


class ShortURL(models.Model):
    """
    Model representing a shortened URL with optional expiration and password protection.
    """
    original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    clicks = models.PositiveIntegerField(default=0)
    expiration = models.DateTimeField(null=True, blank=True)
    last_clicked = models.DateTimeField(null=True, blank=True)
    password = models.CharField(max_length=128, blank=True, null=True)

    def set_password(self, raw_password):
        """
        Hash and store the password for the URL.
        """
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Verify if the provided password matches the stored hash.
        Returns True if no password is set.
        """
        if not self.password:
            return True
        return check_password(raw_password, self.password)

    def is_expired(self):
        """
        Check if the URL has expired based on the expiration datetime.
        """
        if self.expiration:
            return timezone.now() >= self.expiration
        return False

    def __str__(self):
        return self.original_url


class URLClick(models.Model):
    """
    Model to track clicks for ShortURL, storing IP address and user agent.
    Ensures unique clicks per IP per URL.
    """
    url = models.ForeignKey(ShortURL, on_delete=models.CASCADE, related_name='click_logs')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True, null=True)
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('url', 'ip_address')
