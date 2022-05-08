import pandas as pd
from api.models import Bill, Client, Organization
from django.shortcuts import get_object_or_404


class ClientsAndOrganizationsHandlerMixin(object):
    """."""

    def save_clients(self, validated_data):
        """"""
        uploaded_file = dict(validated_data).get('file')
        client_df = pd.read_excel(uploaded_file, sheet_name='client')
        client_names = client_df['name'].to_list()
        for name in client_names:
            client = Client(name=name)
            client.save()

    def save_organizations(self, validated_data):
        """"""
        uploaded_file = dict(validated_data).get('file')
        organization_df = pd.read_excel(uploaded_file, sheet_name='organization')
        all_values_of_rows = organization_df.values.tolist()
        for client_name, organization_name in all_values_of_rows:
            client = get_object_or_404(Client, name=client_name)
            organization = Organization(client=client, name=organization_name)
            organization.save()


class BillsHandlerMixin(object):
    """."""

    def save_bills(self, validated_data):
        """"""
        uploaded_file = dict(validated_data).get('file')
        bills_df = pd.read_excel(uploaded_file, sheet_name=0)
        all_values_of_rows = bills_df.values.tolist()
        for organization_name, number, sum, date in all_values_of_rows:
            organization = get_object_or_404(Organization, name=organization_name)
            client = Bill(organization=organization, number=number, sum=sum, date=date)
            client.save()
