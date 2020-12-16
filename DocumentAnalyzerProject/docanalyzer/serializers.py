from rest_framework import serializers

from .analyzer import runFileMetrics
from .models import FileUpload, FileMetric

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileMetric
        fields = '__all__'

class UploadSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(many=True, read_only=True)

    class Meta:
        model=FileUpload
        fields=['file', 'metrics']

    def create(self, validated_data):
        ip = self.context['request'].META.get('HTTP_X_FORWARDED_FOR').split(',')[0] if self.context['request'].META.get(
            'HTTP_X_FORWARDED_FOR') else self.context['request'].META.get('REMOTE_ADDR')
        file_upload = FileUpload(file=self.validated_data['file'], uploader_ip=ip)
        file_upload.save()
        results = runFileMetrics(file_upload)
        file_upload.is_processed = True
        file_upload.save()
        file_metric = FileMetric(file=file_upload, **results)
        file_metric.save()
        return file_upload
