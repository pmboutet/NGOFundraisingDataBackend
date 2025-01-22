from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.configuration import ConfigurationViewSet
from .views.download import DownloadDatasetView, DatasetStatusView
from .views import GenerateDatasetView

router = DefaultRouter()
router.register(r'configurations', ConfigurationViewSet, basename='configuration')

app_name = 'fundraising'

urlpatterns = [
    path('', include(router.urls)),
    path('generate/', GenerateDatasetView.as_view(), name='generate_dataset'),
    path('datasets/<int:dataset_id>/download/', DownloadDatasetView.as_view(), name='download_dataset'),
    path('datasets/<int:dataset_id>/status/', DatasetStatusView.as_view(), name='dataset_status'),
]