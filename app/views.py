from app.models import Event
from app.serializers import EventSerializer
from app.filters import EventFilter
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from app.pagination import EventPagination


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
