from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.user_serializers import UserSerializer


class CreateCompanyUserView(generics.CreateAPIView):

    def post(self, request: Request, company_id: int) -> Response:
        data = request.data
        serializer = UserSerializer(
            data=data,
            context={"company_id": company_id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
