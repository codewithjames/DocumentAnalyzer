from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from docanalyzer import views

router = routers.DefaultRouter()
router.register(r'upload', views.UploadViewSet, basename='upload')
router.register(r'metrics', views.MetricViewSet, basename='metric')

urlpatterns = [
    path('', include(router.urls)), # Including for simplicity
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include((router.urls, 'api'), namespace='api')), # Normal way to interact with system
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)