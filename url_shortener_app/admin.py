from django.contrib import admin
from url_shortener_app.models import ShortURL

@admin.register(ShortURL)
class UrlAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ['original_url', 'clicks', 'created_at', 'unique_clicks']

    # Fields that are read-only in the admin (not editable)
    readonly_fields = ['clicks', 'unique_clicks', 'created_at']

    # Enable search functionality by the original URL
    search_fields = ['original_url']

    # Enable filtering by creation date
    list_filter = ['created_at']

    def unique_clicks(self, obj):
        """
        Returns the number of unique clicks for this URL.
        Counts distinct IP addresses from click logs.
        """
        return obj.click_logs.values('ip_address').distinct().count()
    
    # Column label in the admin list view
    unique_clicks.short_description = 'Unique Clicks'



