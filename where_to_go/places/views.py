from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Place


def place_details(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    imgs = [img.image.url for img in place.images.all()]

    return JsonResponse(
        {
            "title": place.title,
            "imgs": imgs,
            "description_short": place.short_description,
            "description_long": place.long_description,
            "coordinates": {
                "lat": place.latitude,
                "lng": place.longitude
            }
        },
        json_dumps_params={
            "ensure_ascii": False,
            "indent": 2,
        }
    )


def index(request):
    places = Place.objects.all()

    features = []
    for place in places:
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [place.longitude, place.latitude]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": reverse("place_details", args=[place.id])
            }
        })
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    context = {
        "places_geojson": geojson,
    }

    return render(request, "index.html", context)
