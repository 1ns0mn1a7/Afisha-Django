from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField("Название", max_length=200, unique=True)
    short_description = models.TextField("Краткое описание", blank=True)
    long_description = HTMLField("Полное описание", blank=True)
    longitude = models.FloatField("Долгота")
    latitude = models.FloatField("Широта")

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.title
    

class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Место",
    )
    image = models.ImageField(
        "Картинка",
        upload_to="places",
    )
    position = models.PositiveIntegerField(
        "Позиция",
        default=0,
        blank=False,
        null=False,
        db_index=True
    )

    class Meta:
        ordering = ["position"]
        verbose_name = "Фотография"
        verbose_name_plural = "Фотографии"

    def __str__(self):
        return f"{self.place.title} — {self.position}"
