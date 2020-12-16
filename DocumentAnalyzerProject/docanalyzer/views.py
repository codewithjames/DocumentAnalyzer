from rest_framework import viewsets

from .serializers import UploadSerializer, MetricSerializer
from .models import FileUpload, FileMetric

class UploadViewSet(viewsets.ModelViewSet):
    queryset = FileUpload.objects.all()
    serializer_class = UploadSerializer
    # permission_classes = [permissions.IsAuthenticated] # Added to show support for authentication
    http_method_names = ['get','post', 'head']

class MetricViewSet(viewsets.ModelViewSet):
    queryset = FileMetric.objects.all()
    serializer_class = MetricSerializer
    # permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'head']