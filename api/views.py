from api.mixins import BillsHandlerMixin, ClientsAndOrganizationsHandlerMixin
from api.models import Bill, Client, Organization
from api.serializers import (
    BillSerializer,
    BillsFileSerializer,
    ClientListSerializer,
    ClientsAndOrganizationsFileSerializer,
)
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response


class ClientList(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer


class BillList(generics.ListAPIView):
    serializer_class = BillSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        query_params = dict(self.request.GET)
        for query_param, query_param_value in query_params.items():
            if len(query_param_value) == 1 and ',' in query_param_value[0]:
                query_params[query_param] = query_param_value[0].split(',')
        queryset = Bill.objects.all()
        organization_names = query_params.get('organization_names')
        client_names = query_params.get('client_names')
        if organization_names is not None:
            organizations = Organization.objects.filter(name__in=organization_names)
            queryset = queryset.filter(organization__in=organizations)
        elif client_names is not None:
            clients = Client.objects.filter(name__in=client_names)
            organizations = Organization.objects.filter(client__in=clients)
            queryset = queryset.filter(organization__in=organizations)
        return queryset


class UploadClientsAndOrganizationsFile(ClientsAndOrganizationsHandlerMixin, generics.CreateAPIView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = ClientsAndOrganizationsFileSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        self.save_clients(serializer.validated_data)
        self.save_organizations(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        response = {'message': 'successful'}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class UploadBillsFile(BillsHandlerMixin, generics.CreateAPIView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = BillsFileSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)
        self.save_bills(serializer.validated_data)
        headers = self.get_success_headers(serializer.data)
        response = {'message': 'successful'}
        return Response(response, status=status.HTTP_201_CREATED, headers=headers)
