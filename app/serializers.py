from rest_framework import serializers
from app.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "device_id", "event_type", "severity", "timestamp", "metadata"]


class SeveritySummarySerializer(serializers.Serializer):
    low = serializers.IntegerField(
        default=0, help_text="Count of low-severity registered events"
    )
    medium = serializers.IntegerField(
        default=0, help_text="Count of medium-severity registered events"
    )
    high = serializers.IntegerField(
        default=0, help_text="Count of high-severity registered events"
    )


class EventTypeSummarySerializer(serializers.Serializer):
    motion_detected = serializers.IntegerField(
        default=0, help_text='Count of "motion_detected" registered events'
    )
    intrusion_alert = serializers.IntegerField(
        default=0, help_text='Count of "intrusion_alert" registered events'
    )
    camera_offline = serializers.IntegerField(
        default=0, help_text='Count of "camera_offline" registered events'
    )


class SummarySerializer(serializers.Serializer):
    total_events = serializers.IntegerField(
        default=0, help_text="Count of all registered events"
    )
    by_severity = SeveritySummarySerializer(default=SeveritySummarySerializer)
    by_event_type = EventTypeSummarySerializer(default=EventTypeSummarySerializer)
    most_active_device = serializers.CharField(
        default="",
        help_text="Device ID of the device with the highest amount of registered events",
    )
    high_severity_rate = serializers.FloatField(
        default=0.0,
        help_text="Rate of high-severity events, in relation to events of all severity",
    )
