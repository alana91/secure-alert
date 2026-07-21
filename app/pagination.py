from typing import Any

from rest_framework.pagination import PageNumberPagination, Response


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

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "properties": {
                "next": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": 'http://api.example.org/accounts/?{page_query_param}=cD00ODY%3D"'.format(
                        page_query_param=self.page_query_param
                    ),
                },
                "previous": {
                    "type": "string",
                    "nullable": True,
                    "format": "uri",
                    "example": "http://api.example.org/accounts/?{page_query_param}=cj0xJnA9NDg3".format(
                        page_query_param=self.page_query_param
                    ),
                },
                "total": {
                    "type": "integer",
                    "example": 123,
                },
                "events": schema,
            },
        }
