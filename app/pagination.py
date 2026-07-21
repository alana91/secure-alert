from rest_framework.pagination import PageNumberPagination, Response
from typing import Any


class EventPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data: Any):
        return Response(
            {
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "total": self.page.paginator.count,
                "events": data,
            }
        )
