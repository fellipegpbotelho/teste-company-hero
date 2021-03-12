from rest_framework import generics

from api.serializers.company_serializers import CompanySerializer


class CreateCompanyView(generics.CreateAPIView):
    serializer_class = CompanySerializer
