from django.urls import path
from .views import KYCUploadAPIView

urlpatterns = [
    path('upload/', KYCUploadAPIView.as_view()),
]
