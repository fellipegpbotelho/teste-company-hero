from rest_framework import exceptions, generics
from rest_framework.request import Request
from rest_framework.response import Response

from api.serializers import user_serializers
from users import models


class CreateCompanyUserView(generics.CreateAPIView):
    serializer_class = user_serializers.CreateUserSerializer

    def post(self, request: Request, id: int) -> Response:
        data = request.data
        serializer = user_serializers.CreateUserSerializer(
            data=data,
            context={"company_id": id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class GetUserView(generics.RetrieveAPIView):
    serializer_class = user_serializers.GetUserAndCompanies

    def get(self, request: Request) -> Response:
        try:
            email = request.GET.get("email", "")
            user = models.User.objects.get(email=email)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except models.User.DoesNotExist:
            raise exceptions.ValidationError(
                detail="User not found.",
                code="400",
            )
