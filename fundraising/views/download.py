from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import FileResponse, Http404
from django.conf import settings
from django.core.exceptions import PermissionDenied
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from ..models import GeneratedDataset
import os

@extend_schema(
    tags=['datasets'],
    description='Download generated dataset files (transactions or contacts)',
    parameters=[
        OpenApiParameter(
            name='type',
            type=str,
            location=OpenApiParameter.QUERY,
            description='Type of file to download',
            required=True,
            enum=['transactions', 'contacts'],
            examples=[
                OpenApiExample(
                    'Transactions',
                    value='transactions',
                    description='Download transactions CSV file'
                ),
                OpenApiExample(
                    'Contacts',
                    value='contacts',
                    description='Download contacts CSV file'
                ),
            ]
        ),
    ],
    responses={
        200: OpenApiTypes.BINARY,
        400: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    }
)
class DownloadDatasetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.select_related('configuration').get(pk=dataset_id)
            
            # Check if the user owns this dataset
            if dataset.configuration.created_by != request.user:
                raise PermissionDenied('You do not have permission to download this dataset')
            
            # Get file type from query params
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
            
            if not os.path.exists(file_path):
                return Response(
                    {'error': 'File not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            dataset.download_count += 1
            dataset.save()
            
            response = FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=filename
            )
            response['Content-Type'] = 'text/csv'
            return response
            
        except GeneratedDataset.DoesNotExist:
            raise Http404('Dataset not found')
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    tags=['datasets'],
    description='Get dataset generation status and metadata',
    responses={
        200: OpenApiTypes.OBJECT,
        403: OpenApiTypes.OBJECT,
        404: OpenApiTypes.OBJECT
    }
)
class DatasetStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.select_related('configuration').get(pk=dataset_id)
            
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