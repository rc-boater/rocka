from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("climbs", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="FeatureSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("photo_uploads_enabled", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name_plural": "feature settings"},
        ),
    ]
