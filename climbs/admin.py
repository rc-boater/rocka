from django.contrib import admin
from .models import Climb, ClimbPhoto, FeatureSettings


class ClimbPhotoInline(admin.TabularInline):
    model = ClimbPhoto
    extra = 0


@admin.register(Climb)
class ClimbAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "climbed_on", "discipline", "grade_system", "grade", "sent")
    list_filter = ("discipline", "grade_system", "sent")
    search_fields = ("name", "location", "user__username", "user__email")
    inlines = [ClimbPhotoInline]


@admin.register(FeatureSettings)
class FeatureSettingsAdmin(admin.ModelAdmin):
    fields = ("photo_uploads_enabled", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        return not FeatureSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

