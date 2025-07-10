from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from .views import index, place_details


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('places/<int:place_id>/', place_details, name='place_details'),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
