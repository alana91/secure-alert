from rest_framework import serializers
from app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "device_id", "event_type", "severity", "timestamp", "metadata"]
