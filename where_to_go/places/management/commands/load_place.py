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
    raise ConnectionError(f"Не удалось получить данные с {url} после {retries} попыток.")


class Command(BaseCommand):
    help = "Загружаем данные из JSON по ссылке"

    def add_arguments(self, parser):
        parser.add_argument("json_url", type=str)

    def handle(self, *args, **options):
        json_url = options["json_url"]
        response = fetch_with_retries(json_url)

        try:
            place_info = response.json()
        except requests.exceptions.JSONDecodeError as error:
            self.stderr.write(self.style.ERROR(f"Ошибка парсинга JSON: {error}"))
            return

        place, created = Place.objects.get_or_create(
            title=place_info["title"],
            defaults={
                "short_description": place_info.get("description_short", ""),
                "long_description": place_info.get("description_long", ""),
                "longitude": place_info["coordinates"]["lng"],
                "latitude": place_info["coordinates"]["lat"],
            }
        )

        if not created:
            self.stdout.write(self.style.WARNING(f"Место '{place.title}' уже существует. Пропускаем загрузку."))
            return

        for index, img_url in enumerate(place_info.get("imgs", [])):
            img_response = fetch_with_retries(img_url)
            img_name = os.path.basename(urlsplit(img_url).path)
            image = PlaceImage(place=place, position=index)
            image.image.save(img_name, ContentFile(img_response.content), save=True)

        self.stdout.write(self.style.SUCCESS(f"Загружено место: {place.title}"))
