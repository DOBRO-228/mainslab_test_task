from api import views
from django.urls import path

app_name = 'api'
urlpatterns = [
    path(
        'upload_clients_and_orgs_file/',
        views.UploadClientsAndOrganizationsFile.as_view(),
        name='upload_clients_and_orgs_file',
    ),
    path(
        'upload_bills_file/',
        views.UploadBillsFile.as_view(),
        name='upload_bills_file',
    ),
    path('clients/', views.ClientList.as_view(), name='clients'),
    path('bills/', views.BillList.as_view(), name='bills'),
]
