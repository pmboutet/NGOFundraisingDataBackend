from rest_framework.views import APIView
from rest_framework.response import Response

class GenerateDatasetView(APIView):
    def post(self, request):
        try:
            # Logique de génération de données à implémenter
            return Response({'message': 'Dataset generated successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)