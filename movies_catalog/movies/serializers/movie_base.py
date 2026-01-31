from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from movies.models import Movie


@extend_schema_serializer(
    exclude_fields=("single",),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Movie example #1",
            summary="Movie example",
            description="Detailed movie example",
            value={
                "id": 15,
                "title": "Movie Name",
                "description": "Detailed description of the movie",
                "release_date": "2025-09-26",
                "duration": 95,
                "age_rating": "R",
            },
            # request_only=True, # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
        OpenApiExample(
            "Movie example creation",
            summary="Movie creation body example",
            description="Detailed movie example creation body",
            value={
                "title": "MovieName",
                "description": "Details",
                "release_date": "2025-09-26",
                "duration": 95,
                "age_rating": "R",
            },
            request_only=True,  # signal that example only applies to requests
            # response_only=True, # signal that example only applies to responses
        ),
    ],
)
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            "id",
            "title",
            "description",
            "release_date",
            "duration",
            "age_rating",
        )
