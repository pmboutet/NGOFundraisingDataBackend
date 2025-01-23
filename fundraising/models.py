from django.db import models

class DatasetConfiguration(models.Model):
    name = models.CharField(max_length=100)
    config = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class GeneratedDataset(models.Model):
    configuration = models.ForeignKey(DatasetConfiguration, on_delete=models.CASCADE)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)