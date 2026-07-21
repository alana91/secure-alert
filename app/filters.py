import django_filters

from app.models import Event


class EventFilter(django_filters.FilterSet):
    timestamp_from = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    timestamp_to = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="lte"
    )

    class Meta:
        model = Event
        fields = ["device_id", "severity", "event_type"]


class SummaryFilter(django_filters.FilterSet):
    timestamp_from = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="gte", required=True
    )
    timestamp_to = django_filters.IsoDateTimeFilter(
        field_name="timestamp", lookup_expr="lte", required=True
    )
