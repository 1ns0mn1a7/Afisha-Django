from django.db import models


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    short_description = models.TextField("Краткое описание", blank=True)
    long_description = models.TextField("Полное описание", blank=True)
    longitude = models.FloatField("Долгота", blank=True, null=True)
    latitude = models.FloatField("Широта", blank=True, null=True)

    def __str__(self):
        return self.title
    

class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Место",
    )
    image = models.ImageField("Картинка", upload_to='places')
    position = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.place.title} — {self.position}"
