from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from ..models import GeneratedDataset
import os

class DownloadDatasetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.select_related('configuration').get(pk=dataset_id)
            
            # Check if the user owns this dataset
            if dataset.configuration.created_by != request.user:
                raise PermissionDenied('You do not have permission to download this dataset')
            
            # Get file type from query params (transactions or contacts)
            file_type = request.query_params.get('type', 'transactions')
            
            if file_type == 'transactions':
                file_path = dataset.transactions_file.path
                filename = f'transactions_{dataset_id}.csv'
            elif file_type == 'contacts':
                file_path = dataset.contacts_file.path
                filename = f'contacts_{dataset_id}.csv'
            else:
                return Response(
                    {'error': 'Invalid file type. Must be either "transactions" or "contacts".'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if file exists
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Increment download count
            dataset.download_count += 1
            dataset.save()
            
            # Return file as response
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename
            )
            
            # Add appropriate headers
            response['Content-Type'] = 'text/csv'
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except GeneratedDataset.DoesNotExist:
            raise Http404('Dataset not found')
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DatasetStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.select_related('configuration').get(pk=dataset_id)
            
            # Check if the user owns this dataset
            if dataset.configuration.created_by != request.user:
                raise PermissionDenied('You do not have permission to access this dataset')
            
            return Response({
                'id': dataset.id,
                'status': dataset.configuration.status,
                'created_at': dataset.generated_at,
                'download_count': dataset.download_count,
                'has_transactions': bool(dataset.transactions_file),
                'has_contacts': bool(dataset.contacts_file),
                'configuration_name': dataset.configuration.name,
                'error_message': dataset.configuration.error_message
            })
            
        except GeneratedDataset.DoesNotExist:
            raise Http404('Dataset not found')