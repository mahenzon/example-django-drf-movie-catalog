from django.urls import path, include
from rest_framework.routers import DefaultRouter

from movies import views

router = DefaultRouter()
router.register("movies", views.MovieViewSet)

app_name = "movies"

urlpatterns = [
    path("", include(router.urls)),
]
