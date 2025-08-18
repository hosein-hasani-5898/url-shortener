from rest_framework import serializers
from url_shortener_app.models import ShortURL
from url_shortener_app.api.utils import encode_id


class ClickReportSerializer(serializers.Serializer):
    """
    Serializer for click reports including daily and weekly clicks.
    """
    clicks_today = serializers.IntegerField()
    clicks_week = serializers.IntegerField()


class ShortURLSerializer(serializers.ModelSerializer):
    """
    Serializer for ShortURL model.
    Generates a short code and full short URL, supports password-protected links.
    """
    short_code = serializers.SerializerMethodField()
    short_url = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    unique_clicks = serializers.SerializerMethodField()  # Count of unique users

    class Meta:
        model = ShortURL
        fields = [
            'original_url', 'short_code', 'short_url',
            'clicks', 'unique_clicks', 'expiration', 'password'
        ]
        read_only_fields = ['clicks', 'unique_clicks']

    def create(self, validated_data):
        """
        Create a ShortURL instance and hash the password if provided.
        """
        password = validated_data.pop('password', None)
        short_url = ShortURL.objects.create(**validated_data)
        if password:
            short_url.set_password(password)
            short_url.save(update_fields=['password'])
        return short_url

    def get_short_code(self, obj):
        """
        Generate a short code from the URL's database ID.
        """
        return encode_id(obj.id)

    def get_short_url(self, obj):
        """
        Generate full short URL using request context, if available.
        """
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f"/{encode_id(obj.id)}")
        return encode_id(obj.id)

    def get_unique_clicks(self, obj):
        """
        Return the number of unique users (by IP) who clicked the URL.
        """
        return obj.click_logs.count()
