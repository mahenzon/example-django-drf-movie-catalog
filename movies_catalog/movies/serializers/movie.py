from rest_framework import serializers

from movies.models import AgeRating, Movie
from movies.serializers import AgeRatingSerializer


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


class MovieSerializerExtended(serializers.HyperlinkedModelSerializer):
    age_rating = serializers.HyperlinkedRelatedField(
        view_name="movies:agerating-detail",
        queryset=AgeRating.objects.all(),
    )

    class Meta(MovieSerializer.Meta):
        pass


class MovieDetailSerializerExtended(MovieSerializer):
    age_rating = AgeRatingSerializer(
        many=False,
    )

    class Meta(MovieSerializer.Meta):
        pass
