from rest_framework import serializers

from companies.models import Company

from . import user_serializers


class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "email", "cnpj"]


class GetCompanySerializer(serializers.ModelSerializer):
    users = user_serializers.GetUserSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ["id", "name", "email", "cnpj", "users"]
