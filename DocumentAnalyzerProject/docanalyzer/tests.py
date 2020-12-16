import io
import tempfile
import shutil

from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APITestCase


MEDIA_ROOT = tempfile.mkdtemp()

@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class FileUploadTests(APITestCase):

    def test_file_upload(self):
        """
            Testing that we can upload a file
        """
        url = reverse('api:upload-list')
        file = io.BytesIO(open('./docanalyzer/testfiles/romeoandjuliet.txt', 'rb').read())
        response = self.client.post(url, {'file': file}, format='multipart')
        result = response.json()
        self.assertTrue('metrics' in result)
        self.assertEqual(201, response.status_code)

    def test_file_metrics(self):
        """
            Testing that file uploaded enables a valid metrics result
        """
        url = reverse('api:upload-list')
        file = io.BytesIO(open('./docanalyzer/testfiles/romeoandjuliet.txt', 'rb').read())
        response = self.client.post(url, {'file': file}, format='multipart')
        data = response.json()
        metric_id = data['metrics'][0]['id']
        url = reverse('api:metric-detail', args=[metric_id])
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_file_metrics_is_valid(self):
        """
            Testing that file metrics match what we expect
        """
        url = reverse('api:upload-list')
        file = io.BytesIO(open('./docanalyzer/testfiles/romeoandjuliet.txt', 'rb').read())
        response = self.client.post(url, {'file': file}, format='multipart')
        data = response.json()
        metric_id = data['metrics'][0]['id']
        url = reverse('api:metric-detail', args=[metric_id])
        response = self.client.get(url)
        metrics = response.json()
        self.assertEqual(200, response.status_code)
        del metrics['id'] # Just in case our ID changes we don't want the test to break
        romeo_juliet_metric = {
            "average_length": "4.22",
            "longest_words": ["unenforceability"],
            "number_palindromes": 1684,
            "number_unique_words": 3717,
            "number_words": 22569,
            "file": 1
        }
        self.assertDictEqual(romeo_juliet_metric, metrics)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()