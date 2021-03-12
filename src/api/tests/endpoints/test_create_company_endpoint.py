from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from companies import models


class CreateCompanyEndpointTestCase(APITestCase):

    def setUp(self) -> None:
        self.endpoint = reverse("api:company.create")
        self.data = {
            "name": "Company 01",
            "email": "company01@email.com",
            "cnpj": "123"
        }

    def test_create_new_company(self) -> None:
        self.client.post(path=self.endpoint, data=self.data)
        company_was_created = models.Company.objects \
            .filter(email="company01@email.com") \
            .exists()
        self.assertTrue(company_was_created)

    def test_return_status_code_201(self) -> None:
        response = self.client.post(path=self.endpoint, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_enpoint_return_company_created(self) -> None:
        response = self.client.post(path=self.endpoint, data=self.data)
        company_created = response.json()
        self.assertEqual(company_created.get("name"), self.data.get("name"))
        self.assertEqual(company_created.get("email"), self.data.get("email"))
        self.assertEqual(company_created.get("cnpj"), self.data.get("cnpj"))

    def test_return_status_code_400_if_company_already_exists(self) -> None:
        models.Company.objects.create(**self.data)
        response = self.client.post(path=self.endpoint, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_error_if_company_already_exists(self) -> None:
        models.Company.objects.create(**self.data)
        response = self.client.post(path=self.endpoint, data=self.data)
        errors = response.json()
        self.assertListEqual(errors.get("email"), [
            "company with this email already exists.",
        ])
        self.assertListEqual(errors.get("cnpj"), [
            "company with this cnpj already exists.",
        ])
