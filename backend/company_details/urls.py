from django.urls import path

from . import views

urlpatterns = [
    path('', views.CompanyDetailList.as_view(), name='company_detail_list'),
    path('new', views.CompanyDetailCreate.as_view(), name='company_detail_new'),
    path('edit/<int:pk>', views.CompanyDetailUpdate.as_view(), name='company_detail_edit'),
    path('delete/<int:pk>', views.CompanyDetailDelete.as_view(), name='company_detail_delete'),
    path('delete_by_symbol', views.CompanyDetailDeleteBySymbol.as_view(), name='company_detail_delete_by_symbol'),
]
