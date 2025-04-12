from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import Serializer

from movies.models import AgeRating, Movie
from movies.serializers import (
    AgeRatingDetailSerializer,
    AgeRatingSerializer,
    MovieDetailSerializerExtended,
    MovieSerializer,
)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()

    def get_queryset(self) -> QuerySet:
        qs = self.queryset
        if self.action == "retrieve":
            qs = qs.select_related("age_rating")
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
