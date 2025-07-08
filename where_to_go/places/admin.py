from django.contrib import admin
from .models import Place, PlaceImage
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = PlaceImage
    extra = 1
    readonly_fields = ["preview"]
    fields = ["image", "preview"]

    def preview(self, obj):
        try:
            if obj.image:
                return format_html('<img src="{}" style="max-height: 200px;" />', obj.image.url)
        except Exception as e:
            print(f"[PREVIEW ERROR] {e}")
        return "—"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ("title",)
    inlines = [PlaceImageInline]


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ("place", "position") 
