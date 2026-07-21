from app.models import Event
from app.serializers import EventSerializer, SummarySerializer
from app.filters import EventFilter
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from app.pagination import EventPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from collections import defaultdict


class EventViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    API endpoint that allows security alert Events to be created and viewed.
    """

    queryset = Event.objects.all().order_by("-timestamp")
    serializer_class = EventSerializer
    filterset_class = EventFilter
    pagination_class = EventPagination

    @action(detail=False)
    def summary(self, requests):
        qs = self.get_queryset()
        total = qs.count()
        if total == 0:
            serializer = SummarySerializer({})
            return Response(serializer.data)

        most_active_device = (
            qs.values("device_id")
            .annotate(total=Count("device_id"))
            .order_by("-total")
            .first()
        )
        by_event_type = (
            qs.values("event_type")
            .order_by("event_type")
            .annotate(total=Count("event_type"))
        )
        by_severity = (
            qs.values("severity").order_by("severity").annotate(total=Count("severity"))
        )

        severity_map = defaultdict(lambda: 0)
        for count in by_severity:
            severity_map[count["severity"]] = count["total"]

        event_type_map = defaultdict(lambda: 0)
        for count in by_event_type:
            event_type_map[count["event_type"]] = count["total"]

        high_severity_rate = severity_map["high"] / total

        summary = {
            "total_events": total,
            "by_severity": {
                "low": severity_map["low"],
                "medium": severity_map["medium"],
                "high": severity_map["high"],
            },
            "by_event_type": {
                "motion_detected": event_type_map["motion_detected"],
                "intrusion_alert": event_type_map["intrusion_alert"],
                "camera_offline": event_type_map["camera_offline"],
            },
            "most_active_device": most_active_device["device_id"],
            "high_severity_rate": high_severity_rate,
        }

        serializer = SummarySerializer(summary)

        return Response(serializer.data)
