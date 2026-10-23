import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models
import climbs.models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Climb",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("climbed_on", models.DateField()), ("name", models.CharField(max_length=200)),
                ("location", models.CharField(blank=True, max_length=250)),
                ("discipline", models.CharField(choices=[("boulder", "Bouldering"), ("sport", "Sport"), ("trad", "Trad"), ("top_rope", "Top rope"), ("ice", "Ice"), ("alpine", "Alpine")], max_length=20)),
                ("grade_system", models.CharField(choices=[("V", "V Scale"), ("YDS", "Yosemite Decimal System"), ("French", "French sport"), ("UIAA", "UIAA"), ("Font", "Fontainebleau")], max_length=10)),
                ("grade", models.CharField(max_length=20)),
                ("attempts", models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)])),
                ("sent", models.BooleanField(default=True)), ("notes", models.TextField(blank=True, max_length=4000)),
                ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="climbs", to=settings.AUTH_USER_MODEL)),
            ], options={"ordering": ["-climbed_on", "-created_at"]},
        ),
        migrations.AddIndex(model_name="climb", index=models.Index(fields=["user", "climbed_on"], name="climbs_cli_user_id_0b5f24_idx")),
        migrations.AddIndex(model_name="climb", index=models.Index(fields=["user", "grade_system"], name="climbs_cli_user_id_8ae3f5_idx")),
        migrations.CreateModel(
            name="ClimbPhoto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to=climbs.models.climb_photo_path)), ("caption", models.CharField(blank=True, max_length=250)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("climb", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="photos", to="climbs.climb")),
            ], options={"ordering": ["uploaded_at"]},
        ),
    ]
