from django.urls import path

from . import views

urlpatterns = [
    path('', views.CompanyDetailList.as_view(), name='company_detail_list'),
    path('new', views.CompanyDetailCreate.as_view(), name='company_detail_new'),
    path('edit/<int:company_id>', views.CompanyDetailUpdate.as_view(), name='company_detail_edit'),
    path('delete/<int:company_id>', views.CompanyDetailDelete.as_view(), name='company_detail_delete'),
]