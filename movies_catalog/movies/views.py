from rest_framework import viewsets

from movies.models import AgeRating, Movie
from movies.serializers import AgeRatingSerializer, MovieSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class AgeRatingViewSet(viewsets.ModelViewSet):
    queryset = AgeRating.objects.all()
    serializer_class = AgeRatingSerializer
