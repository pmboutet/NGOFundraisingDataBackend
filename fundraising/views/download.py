from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import GeneratedDataset

class GenerateDatasetView(APIView):
    def post(self, request):
        # TODO: Implement dataset generation
        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)