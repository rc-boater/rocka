from rest_framework import serializers
from .models import Climb, ClimbPhoto, FeatureSettings


class ClimbPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClimbPhoto
        fields = ("id", "image", "caption", "uploaded_at")
        read_only_fields = ("id", "uploaded_at")


class ClimbSerializer(serializers.ModelSerializer):
    photos = ClimbPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Climb
        fields = ("id", "climbed_on", "name", "location", "discipline", "grade_system", "grade", "attempts", "sent", "notes", "photos", "created_at", "updated_at")
        read_only_fields = ("id", "photos", "created_at", "updated_at")


class FeatureSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureSettings
        fields = ("photo_uploads_enabled",)

