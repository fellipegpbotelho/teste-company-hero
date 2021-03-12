from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from companies import models as models_company
from users import models as models_user


class GetCompanyEndpointTestCase(APITestCase):

    def setUp(self) -> None:
        self.company = models_company.Company.objects.create(
            name="Company 01",
            email="company01@email.com",
            cnpj="36.033.000/0001-35"
        )
        kwargs = {"id": self.company.pk}
        self.endpoint = reverse("api:company.show", kwargs=kwargs)

    def test_return_company_attributes(self) -> None:
        response = self.client.get(path=self.endpoint)
        attributes = response.json()
        self.assertEqual(attributes.get("id"), self.company.pk)
        self.assertEqual(attributes.get("name"), self.company.name)
        self.assertEqual(attributes.get("email"), self.company.email)
        self.assertEqual(attributes.get("cnpj"), self.company.cnpj)

    def test_return_status_code_200(self) -> None:
        response = self.client.get(path=self.endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_company_without_users_related(self) -> None:
        response = self.client.get(path=self.endpoint)
        attributes = response.json()
        self.assertEqual(attributes.get("users"), [])

    def test_return_company_with_users_related(self) -> None:
        user = models_user.User.objects.create(
            name="User 01",
            email="user01@email.com",
        )
        self.company.users.add(user)
        self.company.save()
        response = self.client.get(path=self.endpoint)
        attributes = response.json()
        self.assertEqual(attributes.get("users")[0], {
            "id": user.pk,
            "name": user.name,
            "email": user.email,
        })
