from django.urls import path
from .views import GeminiAPIView, ProjectOptimizationAPIView

urlpatterns = [
    path('ai-helper/', GeminiAPIView.as_view(), name='ai_helper'),
    path('optimize-ai/', ProjectOptimizationAPIView.as_view(), name='ai_helper'),
]
