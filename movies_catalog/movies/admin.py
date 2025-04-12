from django.contrib import admin

from movies.models import AgeRating, Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "description",
        "release_date",
        "duration",
    )
    list_display_links = (
        "id",
        "title",
    )
    list_filter = (
        "title",
        "release_date",
    )
    search_fields = (
        "title",
        "description",
    )


@admin.register(AgeRating)
class AgeRatingAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_display_links = ("name",)
    list_filter = ("name",)
    search_fields = (
        "name",
        "description",
    )
