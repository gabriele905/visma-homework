from django.urls import path

from . import views

urlpatterns = [
    path('<int:company_id>', views.HistoricalDataList.as_view(), name='company_historical_data_view'),
    path('<int:company_id>/sync', views.HistoricalDataSync.as_view(), name='company_historical_data_sync'),
]
