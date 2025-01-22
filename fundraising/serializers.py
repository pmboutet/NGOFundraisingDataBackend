from rest_framework import serializers
from .models import DatasetConfiguration, GeneratedDataset

class GeneratedDatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedDataset
        fields = ['id', 'transactions_file', 'contacts_file', 'generated_at', 'download_count']
        read_only_fields = ['id', 'generated_at', 'download_count']

class DatasetConfigurationSerializer(serializers.ModelSerializer):
    generated_datasets = GeneratedDatasetSerializer(many=True, read_only=True)
    
    class Meta:
        model = DatasetConfiguration
        fields = ['id', 'name', 'config_file', 'created_at', 'status', 'error_message', 'generated_datasets']
        read_only_fields = ['id', 'created_at', 'status', 'error_message']
