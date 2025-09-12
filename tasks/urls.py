from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from .views_ai import AudioUploadView

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("upload-audio/", AudioUploadView.as_view(), name="upload-audio"),
]
