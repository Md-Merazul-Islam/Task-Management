
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('auths.urls')),
    path('api/v1/task/', include('task.urls')),
    path('api/v1/open-ai/', include('ai_help.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
