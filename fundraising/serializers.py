from rest_framework import serializers
from .models import DatasetConfiguration, GeneratedDataset

class DatasetConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetConfiguration
        fields = '__all__'