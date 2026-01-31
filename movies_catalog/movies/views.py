from textwrap import dedent

from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import status, viewsets
from rest_framework.serializers import Serializer

from movies.models import AgeRating, Movie
from movies.serializers import (
    AgeRatingDetailSerializer,
    AgeRatingSerializer,
    MovieDetailSerializerExtended,
    MovieSerializer,
)

INCLUDE_MOVIE_RELATIONS_QUERY_PARAM = OpenApiParameter(
    "include",
    OpenApiTypes.STR,
    # OpenApiParameter.QUERY,
    description="include age_rating and genre",
    default="1",
)


@extend_schema_view(
    list=extend_schema(
        description=dedent(
            """
            ## List available movies

            Example list:

            - one
            - two
            - three with inner:
                - a
                - b
                - c
            - four

            **Example API call:**

            ```bash
            curl -X 'GET' 'http://127.0.0.1:8000/api/movies/'
            ```
            """,
        ),
        parameters=[
            INCLUDE_MOVIE_RELATIONS_QUERY_PARAM,
        ],
    ),
    create=extend_schema(
        responses={
            status.HTTP_201_CREATED: MovieSerializer,
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response="application/json",
                examples=[
                    OpenApiExample(
                        name="Invalid FK example",
                        value={
                            "age_rating": [
                                'Invalid pk "foobar" - object does not exist.',
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Missing required fields",
                        value={
                            "title": [
                                "This field is required.",
                            ],
                        },
                    ),
                ],
            ),
        },
    ),
    retrieve=extend_schema(
        description=dedent(
            """
            ## Retrieve Movie details by id

            Returns movie details. Use the `include` query parameter to
            include nested `age_rating` and `genres` relationships.

            **Example API call (without include):**

            ```bash
            curl -X 'GET' 'http://127.0.0.1:8000/api/movies/1/'
            ```

            **Example API call (with include):**

            ```bash
            curl -X 'GET' 'http://127.0.0.1:8000/api/movies/1/?include=1'
            ```
            """,
        ),
        parameters=[
            INCLUDE_MOVIE_RELATIONS_QUERY_PARAM,
        ],
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                # response=MovieDetailSerializerExtended,
                response="application/json",
                description="Movie details (without nested relations)",
                examples=[
                    OpenApiExample(
                        name="Response without include",
                        value={
                            "id": 1,
                            "title": "Movie Name",
                            "description": "Movie description",
                            "release_date": "2025-09-26",
                            "duration": 95,
                            "age_rating": "R",
                        },
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="Response with include=1",
                        value={
                            "id": 1,
                            "title": "Movie Name",
                            "description": "Movie description",
                            "release_date": "2025-09-26",
                            "duration": 95,
                            "age_rating": {
                                "id": 1,
                                "symbol": "R",
                                "description": "Restricted",
                            },
                            "genres": [
                                {"id": 1, "name": "Action"},
                                {"id": 2, "name": "Drama"},
                            ],
                        },
                        response_only=True,
                    ),
                ],
            ),
        },
    ),
)
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_queryset(self) -> QuerySet:
        qs = self.queryset
        # if self.action == "retrieve":
        if self.request.method == "GET" and self.request.GET.get("include"):
            qs = qs.select_related("age_rating")
            qs = qs.prefetch_related("genres")
        return qs

    def get_serializer_class(self) -> type[Serializer]:
        if self.request.GET.get("include"):
            # if self.action == "retrieve":
            #     return MovieDetailSerializerExtended
            return MovieDetailSerializerExtended
        return MovieSerializer


class AgeRatingViewSet(viewsets.ModelViewSet):
    queryset = AgeRating.objects.all()

    def get_queryset(self) -> QuerySet:
        qs = self.queryset
        if self.action == "retrieve":
            qs = qs.prefetch_related("movies")
        return qs

    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "retrieve":
            return AgeRatingDetailSerializer
        return AgeRatingSerializer
