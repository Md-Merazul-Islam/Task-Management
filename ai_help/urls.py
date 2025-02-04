from django.urls import path
from .views import GeminiAPIView

urlpatterns = [
    path('ai-helper/', GeminiAPIView.as_view(), name='ai_helper'),
]
