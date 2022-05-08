import os

import pandas as pd
from api.models import Bill, Client
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class ClientsAndOrganizationsFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, uploaded_file):
        _, current_extension = os.path.splitext(uploaded_file.name)
        expected_extensions = ['.xlsx']
        if current_extension not in expected_extensions:
            message = 'Вы загрузили файл с расширением {0}. Ожидаемые расширения: {1}'.format(
                current_extension,
                ' ,'.join(expected_extensions),
            )
            raise ValidationError({'error': message})
        return uploaded_file

    def validate(self, uploaded_file):
        excel_file = pd.ExcelFile(dict(uploaded_file).get('file'))
        self.validate_file_structure(excel_file)
        self.validate_clients_in_sheet(excel_file)
        self.validate_organizations_in_sheet(excel_file)
        return uploaded_file

    def validate_file_structure(self, excel_file):
        expected_sheet_names = ['client', 'organization']
        if excel_file.sheet_names != expected_sheet_names:
            message = "В файле должно быть ровно 2 листа с названиями '{0}' и '{1}'.".format(
                expected_sheet_names[0],
                expected_sheet_names[1],
            )
            raise ValidationError({'error': message})
        client_df = excel_file.parse('client')
        if client_df.columns.values.tolist() != ['name']:
            message = "В листе 'client' должна быть ровно 1 колонка с названием 'name'."
            raise ValidationError({'error': message})
        organization_df = excel_file.parse('organization')
        if organization_df.columns.values.tolist() != ['client_name', 'name']:
            message = "В листе 'organization' должно быть ровно 2 колонки с названиями 'client_name' и 'name'."
            raise ValidationError({'error': message})

    def validate_clients_in_sheet(self, excel_file):
        client_df = excel_file.parse('client')
        client_names = client_df['name'].to_list()
        for name in client_names:
            if not isinstance(name, str):
                message = "Все значения в листе 'client' в колонке 'name' должны быть строками."
                raise ValidationError({'error': message})

    def validate_organizations_in_sheet(self, excel_file):
        organization_df = excel_file.parse('organization')
        client_names = organization_df['client_name'].to_list()
        for client_name in client_names:
            if not isinstance(client_name, str):
                message = "Все значения в листе 'organization' в колонке 'client_name' должны быть строками."
                raise ValidationError({'error': message})
        organization_names = organization_df['name'].to_list()
        for organization_name in organization_names:
            if not isinstance(organization_name, str):
                message = "Все значения в листе 'organization' в колонке 'name' должны быть строками."
                raise ValidationError({'error': message})


class BillsFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, uploaded_file):
        _, current_extension = os.path.splitext(uploaded_file.name)
        expected_extensions = ['.xlsx']
        if current_extension not in expected_extensions:
            message = 'Вы загрузили файл с расширением {0}. Ожидаемые расширения: {1}'.format(
                current_extension,
                ' ,'.join(expected_extensions),
            )
            raise ValidationError({'error': message})
        return uploaded_file


class ClientListSerializer(serializers.ModelSerializer):
    organizations_amount = serializers.SerializerMethodField('get_organizations_amount')
    income = serializers.SerializerMethodField('get_income')

    def get_organizations_amount(self, client):
        return len(client.organizations.all())

    def get_income(self, client):
        income = 0
        for organization in client.organizations.all():
            for bill in organization.bills.all():
                income += bill.sum
        return income

    class Meta:
        model = Client
        fields = ['name', 'organizations_amount', 'income']


class BillSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(slug_field='name', read_only='True')

    class Meta:
        model = Bill
        fields = ['organization', 'number', 'sum', 'date']
