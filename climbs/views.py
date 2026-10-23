from collections import defaultdict
from django.db.models import Count
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Climb, ClimbPhoto, FeatureSettings
from .serializers import ClimbSerializer, ClimbPhotoSerializer, FeatureSettingsSerializer


class UserClimbMixin:
    def get_queryset(self):
        return Climb.objects.filter(user=self.request.user).prefetch_related("photos")


class ClimbListCreateView(UserClimbMixin, generics.ListCreateAPIView):
    serializer_class = ClimbSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClimbDetailView(UserClimbMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClimbSerializer


class ClimbPhotoCreateView(UserClimbMixin, APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        if not FeatureSettings.load().photo_uploads_enabled:
            return Response(
                {"detail": "Photo uploads are currently disabled by the site administrator."},
                status=status.HTTP_403_FORBIDDEN,
            )
        climb = self.get_queryset().filter(pk=pk).first()
        if climb is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        if "image" not in request.FILES:
            raise ValidationError({"image": "Upload an image file."})
        image = request.FILES["image"]
        if image.size > 10 * 1024 * 1024:
            raise ValidationError({"image": "Images must be 10 MB or smaller."})
        serializer = ClimbPhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(climb=climb)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClimbPhotoDetailView(APIView):
    def delete(self, request, pk, photo_pk):
        photo = ClimbPhoto.objects.filter(pk=photo_pk, climb_id=pk, climb__user=request.user).first()
        if photo is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        photo.image.delete(save=False)
        photo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProgressView(APIView):
    """Returns chart-ready completion counts grouped by date and grade system."""
    def get(self, request):
        climbs = Climb.objects.filter(user=request.user, sent=True)
        grade_system = request.query_params.get("grade_system")
        if grade_system:
            climbs = climbs.filter(grade_system=grade_system)
        rows = climbs.values("climbed_on", "grade_system").annotate(count=Count("id")).order_by("climbed_on")
        by_system = defaultdict(list)
        for row in rows:
            by_system[row["grade_system"]].append({"date": row["climbed_on"], "count": row["count"]})
        return Response({"series": [{"grade_system": system, "points": points} for system, points in by_system.items()]})


class FeatureSettingsView(APIView):
    def get(self, request):
        return Response(FeatureSettingsSerializer(FeatureSettings.load()).data)

