from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from ..models import DatasetConfiguration
from ..serializers import DatasetConfigurationSerializer
import yaml

class ConfigurationViewSet(viewsets.ModelViewSet):
    serializer_class = DatasetConfigurationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only configurations owned by the current user"""
        return DatasetConfiguration.objects.filter(
            created_by=self.request.user
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        """Validate YAML and create configuration"""
        # Validate YAML format
        config_file = self.request.FILES.get('config_file')
        try:
            yaml_content = yaml.safe_load(config_file)
            self._validate_config_structure(yaml_content)
            # Reset file pointer for saving
            config_file.seek(0)
            serializer.save(created_by=self.request.user)
        except yaml.YAMLError as e:
            raise serializers.ValidationError({'config_file': f'Invalid YAML format: {str(e)}'})
        except ValueError as e:
            raise serializers.ValidationError({'config_file': str(e)})
    
    def perform_update(self, serializer):
        """Validate YAML and update configuration"""
        config_file = self.request.FILES.get('config_file')
        if config_file:
            try:
                yaml_content = yaml.safe_load(config_file)
                self._validate_config_structure(yaml_content)
                config_file.seek(0)
            except yaml.YAMLError as e:
                raise serializers.ValidationError({'config_file': f'Invalid YAML format: {str(e)}'})
            except ValueError as e:
                raise serializers.ValidationError({'config_file': str(e)})
        
        serializer.save()
    
    @action(detail=True, methods=['post'])
    def validate(self, request, pk=None):
        """Validate a configuration without saving it"""
        config_file = request.FILES.get('config_file')
        if not config_file:
            return Response(
                {'error': 'No configuration file provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            yaml_content = yaml.safe_load(config_file)
            self._validate_config_structure(yaml_content)
            return Response({'status': 'valid'}, status=status.HTTP_200_OK)
        except (yaml.YAMLError, ValueError) as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def _validate_config_structure(self, config):
        """Validate the structure of the configuration YAML"""
        required_fields = ['YEARS', 'FIRST_YEAR', 'CHANNELS']
        for field in required_fields:
            if field not in config:
                raise ValueError(f'Missing required field: {field}')
        
        # Validate channels structure
        channels = config['CHANNELS']
        if not isinstance(channels, dict):
            raise ValueError('CHANNELS must be a dictionary')
            
        for channel_name, channel_data in channels.items():
            required_channel_fields = ['campaigns', 'duration', 'cost_per_reach']
            for field in required_channel_fields:
                if field not in channel_data:
                    raise ValueError(f'Channel {channel_name} missing required field: {field}')
            
            # Validate campaign types
            campaigns = channel_data['campaigns']
            if not isinstance(campaigns, dict):
                raise ValueError(f'Campaigns for channel {channel_name} must be a dictionary')
                
            for campaign_type in campaigns.keys():
                if campaign_type not in ['prospecting', 'retention']:
                    raise ValueError(f'Invalid campaign type in channel {channel_name}: {campaign_type}')
