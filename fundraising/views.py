from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import yaml
from .models import DatasetConfiguration, GeneratedDataset
from .serializers import DatasetConfigurationSerializer
from .generator import FundraisingDataGenerator

class GenerateDatasetView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = DatasetConfigurationSerializer(data=request.data)
        
        if serializer.is_valid():
            config = serializer.save(created_by=request.user)
            
            try:
                # Parse YAML configuration
                config_data = yaml.safe_load(config.config_file)
                
                # Update status
                config.status = 'processing'
                config.save()
                
                # Generate data
                generator = FundraisingDataGenerator(config_data)
                transactions_df, contacts_df = generator.generate()
                
                # Save files
                transactions_path = f'datasets/transactions/{config.id}_transactions.csv'
                contacts_path = f'datasets/contacts/{config.id}_contacts.csv'
                
                transactions_df.to_csv(f'media/{transactions_path}', index=False)
                contacts_df.to_csv(f'media/{contacts_path}', index=False)
                
                # Create dataset record
                dataset = GeneratedDataset.objects.create(
                    configuration=config,
                    transactions_file=transactions_path,
                    contacts_file=contacts_path
                )
                
                # Update status
                config.status = 'completed'
                config.save()
                
                return Response({
                    'status': 'success',
                    'dataset_id': dataset.id
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                config.status = 'failed'
                config.error_message = str(e)
                config.save()
                return Response({
                    'status': 'error',
                    'message': str(e)
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)