from django.db import models


class FileUpload(models.Model):
    file = models.FileField(upload_to='docanalyzer/')
    uploader_ip = models.GenericIPAddressField(null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

class FileMetric(models.Model):
    file = models.ForeignKey(FileUpload, related_name='metrics', on_delete=models.CASCADE)
    average_length = models.DecimalField(max_digits=18, decimal_places=2)
    longest_words = models.JSONField()
    number_palindromes = models.IntegerField()
    number_unique_words = models.IntegerField()
    number_words = models.IntegerField()