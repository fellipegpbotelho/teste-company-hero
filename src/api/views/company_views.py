from rest_framework import generics

from api.serializers import company_serializers
from companies import models


class CreateCompanyView(generics.CreateAPIView):
    serializer_class = company_serializers.CreateCompanySerializer


class GetCompanyView(generics.RetrieveAPIView):
    serializer_class = company_serializers.GetCompanySerializer
    queryset = models.Company.objects.all()
    lookup_field = "id"
