from rest_framework import viewsets
from ..models import DatasetConfiguration
from ..serializers import DatasetConfigurationSerializer

class ConfigurationViewSet(viewsets.ModelViewSet):
    queryset = DatasetConfiguration.objects.all()
    serializer_class = DatasetConfigurationSerializer