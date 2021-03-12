from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers.user_serializers import CreateUserSerializer


class CreateCompanyUserView(generics.CreateAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request: Request, id: int) -> Response:
        data = request.data
        serializer = CreateUserSerializer(
            data=data,
            context={"company_id": id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
