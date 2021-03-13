from django.urls import reverse
from django.utils.http import urlencode
from rest_framework import status
from rest_framework.test import APITestCase

from companies import models as models_company
from users import models as models_user


class GetUserEndpointTestCase(APITestCase):

    def setUp(self) -> None:
        self.company = models_company.Company.objects.create(
            name="Company 01",
            email="company01@email.com",
            cnpj="36.033.000/0001-35"
        )
        self.user = models_user.User.objects.create(
            name="User 01",
            email="user01@email.com",
        )
        self.endpoint = reverse("api:user.show") + "?" +  \
            urlencode({"email": self.user.email})

    def test_return_user_by_email(self) -> None:
        response = self.client.get(path=self.endpoint)
        attributes = response.json()
        self.assertEqual(attributes.get("id"), self.user.pk)
        self.assertEqual(attributes.get("name"), self.user.name)
        self.assertEqual(attributes.get("email"), self.user.email)

    def test_return_status_code_200(self) -> None:
        response = self.client.get(path=self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_status_code_400_if_user_do_not_exist(self) -> None:
        self.endpoint = reverse("api:user.show") + "?" +  \
            urlencode({"email": "dummy@email.com"})
        response = self.client.get(path=self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_error_message_if_user_do_not_exist(self) -> None:
        self.endpoint = reverse("api:user.show") + "?" +  \
            urlencode({"email": "dummy@email.com"})
        response = self.client.get(path=self.endpoint)
        error = response.json()
        self.assertEqual(error, ["User not found."])

    def test_return_user_with_companies_related(self) -> None:
        self.company.users.add(self.user)
        self.company.save()
        response = self.client.get(path=self.endpoint)
        attributes = response.json()
        self.assertEqual(attributes.get("companies")[0], {
            "id": self.company.pk,
            "name": self.company.name,
            "email": self.company.email,
            "cnpj": self.company.cnpj,
        })
