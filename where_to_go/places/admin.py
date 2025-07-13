from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

from .models import Place, PlaceImage


IMAGE_PREVIEW_MAX_HEIGHT_PX = 200
IMAGE_PREVIEW_MAX_WIDTH_PX = 300


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ["preview"]
    fields = ["image", "preview"]

    def preview(self, obj):
        try:
            if obj.image:
                return format_html(
                    "<img src='{}' style='max-height:{}px; max-width:{}px;' />",
                    obj.image.url,
                    IMAGE_PREVIEW_MAX_HEIGHT_PX,
                    IMAGE_PREVIEW_MAX_WIDTH_PX
                )
        except Exception as error:
            print(f"[PREVIEW ERROR] {error}")
        return "—"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ("place", "position")
    autocomplete_fields = ["place"]
