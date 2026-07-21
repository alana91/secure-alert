from django.db import models
from django.core.validators import MinLengthValidator


class Event(models.Model):
    EVENT_CHOICES = [
        ("motion_detected", "motion_detected"),
        ("intrusion_alert", "intrusion_alert"),
        ("camera_offline", "camera_offline"),
    ]

    SEVERITY_CHOICES = [("low", "low"), ("medium", "medium"), ("high", "high")]

    device_id = models.CharField(
        null=False,
        blank=False,
        max_length=64,
        validators=[MinLengthValidator(limit_value=3)],
        help_text="ID of the device that originated the event",
    )
    event_type = models.CharField(
        null=False, blank=False, choices=EVENT_CHOICES, help_text="Event type"
    )
    severity = models.CharField(
        null=False,
        blank=False,
        choices=SEVERITY_CHOICES,
        help_text="Event severity classification",
    )
    timestamp = models.DateTimeField(
        null=False,
        blank=False,
        help_text="Date/time of event occurrence, given by the originating device",
    )
    metadata = models.JSONField(
        null=True, blank=False, help_text="Optional event metadata"
    )
