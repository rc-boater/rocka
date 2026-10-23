from django.urls import path
from .views import ClimbDetailView, ClimbListCreateView, ClimbPhotoCreateView, ClimbPhotoDetailView, FeatureSettingsView, ProgressView

urlpatterns = [
    path("", ClimbListCreateView.as_view()),
    path("features/", FeatureSettingsView.as_view()),
    path("progress/", ProgressView.as_view()),
    path("<int:pk>/", ClimbDetailView.as_view()),
    path("<int:pk>/photos/", ClimbPhotoCreateView.as_view()),
    path("<int:pk>/photos/<int:photo_pk>/", ClimbPhotoDetailView.as_view()),
]

