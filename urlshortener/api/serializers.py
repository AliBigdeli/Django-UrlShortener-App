from rest_framework import serializers
from urlshortener.models import Shortener


class ShortenerSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(read_only=True)

    class Meta:
        model = Shortener
        fields = "__all__"
