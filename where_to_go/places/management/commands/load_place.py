import requests
import os
import time
from urllib.parse import urlsplit
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from places.models import Place, PlaceImage


def fetch_with_retries(url, retries=3, delay=2):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; MyDjangoBot/1.0)"
    }
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as error:
            print(f"[WARNING] Ошибка запроса: {error} (попытка {attempt + 1}/{retries})")
            time.sleep(delay)
    return None


class Command(BaseCommand):
    help = "Загружаем данные из JSON по ссылке"

    def add_arguments(self, parser):
        parser.add_argument("json_url", type=str)

    def handle(self, *args, **options):
        json_url = options["json_url"]
        response = fetch_with_retries(json_url)

        try:
            place_json = response.json()
        except requests.exceptions.JSONDecodeError as error:
            self.stderr.write(self.style.ERROR(f"Ошибка парсинга JSON: {error}"))
            return

        place, created = Place.objects.get_or_create(
            title=place_json["title"],
            defaults={
                "short_description": place_json.get("description_short", ""),
                "long_description": place_json.get("description_long", ""),
                "longitude": place_json["coordinates"]["lng"],
                "latitude": place_json["coordinates"]["lat"],
            }
        )

        if not created:
            self.stdout.write(self.style.WARNING(f"Место '{place.title}' уже существует. Пропускаем загрузку."))
            return

        for index, img_url in enumerate(place_json.get("imgs", [])):
            try:
                img_response = fetch_with_retries(img_url)
                img_name = os.path.basename(urlsplit(img_url).path)

                PlaceImage.objects.create(
                    place=place,
                    position=index,
                    image=ContentFile(img_response.content, name=img_name)
                )
            except requests.exceptions.RequestException as error:
                self.stderr.write(self.style.ERROR(
                    f"[Ошибка] Не удалось загрузить изображение: {img_url}\nПричина: {error}"
                ))
                continue

        self.stdout.write(self.style.SUCCESS(f"Загружено место: {place.title}"))
