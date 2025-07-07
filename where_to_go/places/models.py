from django.db import models


class Place(models.Model):
    title = models.CharField("Название", max_length=200)
    short_description = models.TextField("Краткое описание", blank=True)
    long_description = models.TextField("Полное описание", blank=True)
    longitude = models.FloatField("Долгота", blank=True, null=True)
    latitude = models.FloatField("Широта", blank=True, null=True)

    def __str__(self):
        return self.title