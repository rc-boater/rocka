from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Climb(models.Model):
    class GradeSystem(models.TextChoices):
        V_SCALE = "V", "V Scale"
        YDS = "YDS", "Yosemite Decimal System"
        FRENCH = "French", "French sport"
        UIAA = "UIAA", "UIAA"
        FONT = "Font", "Fontainebleau"

    class Discipline(models.TextChoices):
        BOULDER = "boulder", "Bouldering"
        SPORT = "sport", "Sport"
        TRAD = "trad", "Trad"
        TOP_ROPE = "top_rope", "Top rope"
        ICE = "ice", "Ice"
        ALPINE = "alpine", "Alpine"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="climbs")
    climbed_on = models.DateField()
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=250, blank=True)
    discipline = models.CharField(max_length=20, choices=Discipline.choices)
    grade_system = models.CharField(max_length=10, choices=GradeSystem.choices)
    grade = models.CharField(max_length=20)
    attempts = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(999)])
    sent = models.BooleanField(default=True)
    notes = models.TextField(blank=True, max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-climbed_on", "-created_at"]
        indexes = [models.Index(fields=["user", "climbed_on"]), models.Index(fields=["user", "grade_system"])]

    def __str__(self):
        return f"{self.name} ({self.grade})"


class FeatureSettings(models.Model):
    """The singleton record that controls site-wide product features."""
    photo_uploads_enabled = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "feature settings"

    @classmethod
    def load(cls):
        settings, _ = cls.objects.get_or_create(pk=1)
        return settings

    def __str__(self):
        return "Feature settings"


def climb_photo_path(instance, filename):
    return f"climbs/{instance.climb.user_id}/{instance.climb_id}/{filename}"


class ClimbPhoto(models.Model):
    climb = models.ForeignKey(Climb, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to=climb_photo_path)
    caption = models.CharField(max_length=250, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["uploaded_at"]

