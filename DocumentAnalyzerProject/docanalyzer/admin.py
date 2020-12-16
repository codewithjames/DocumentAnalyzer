from django.contrib import admin
from .models import FileUpload, FileMetric

admin.site.register(FileUpload)
admin.site.register(FileMetric)