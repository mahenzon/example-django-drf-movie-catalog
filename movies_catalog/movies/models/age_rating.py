from django.db import models


class AgeRating(models.Model):
    name = models.CharField(
        max_length=10,
        primary_key=True,
    )
    description = models.TextField(
        null=False,
        blank=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name
