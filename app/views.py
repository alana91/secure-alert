from app.models import Event
from app.serializers import EventSerializer
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


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
