from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import GeneratedDataset

class DownloadDatasetView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.get(id=dataset_id)
            return Response(dataset.data)
        except GeneratedDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

class DatasetStatusView(APIView):
    def get(self, request, dataset_id):
        try:
            dataset = GeneratedDataset.objects.get(id=dataset_id)
            return Response({'status': 'completed' if dataset.data else 'processing'})
        except GeneratedDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)

class GenerateDatasetView(APIView):
    def post(self, request):
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)