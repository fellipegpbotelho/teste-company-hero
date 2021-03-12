from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from companies import models as models_company
from users import models as models_user


class CreateCompanyUserEndpointTestCase(APITestCase):

    def setUp(self) -> None:
        self.company = models_company.Company.objects.create(
            name="Company 01",
            email="company01@email.com",
            cnpj="36.033.000/0001-35"
        )
        kwargs = {"company_id": self.company.pk}
        self.endpoint = reverse("api:company.user.create", kwargs=kwargs)
        self.data = {
            "name": "User 01",
            "email": "user01@email.com",
        }

    def test_create_new_user(self) -> None:
        self.client.post(path=self.endpoint, data=self.data)
        user_was_created = models_user.User.objects \
            .filter(email=self.data.get("email")) \
            .exists()
        self.assertTrue(user_was_created)

    def test_relates_user_with_company(self) -> None:
        self.client.post(path=self.endpoint, data=self.data)
        user_created = models_user.User.objects.get(
            email=self.data.get("email"),
        )
        self.assertEqual(user_created.company_set.first(), self.company)

    def test_return_status_code_200(self) -> None:
        response = self.client.post(path=self.endpoint, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_user_created(self) -> None:
        response = self.client.post(path=self.endpoint, data=self.data)
        user_created = response.json()
        self.assertIsNotNone(user_created.get("id"))
        self.assertEqual(user_created.get("name"), self.data.get("name"))
        self.assertEqual(user_created.get("email"), self.data.get("email"))

    def test_return_status_code_400_if_company_do_not_exists(self) -> None:
        self.endpoint = reverse(
            "api:company.user.create",
            kwargs={"company_id": 0},
        )
        response = self.client.post(path=self.endpoint, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_error_message_if_company_do_not_exists(self) -> None:
        self.endpoint = reverse(
            "api:company.user.create",
            kwargs={"company_id": 0},
        )
        response = self.client.post(path=self.endpoint, data=self.data)
        error = response.json()
        self.assertListEqual(error, ["Company not found."])

    def test_do_not_create_a_new_user_if_already_exist(self):
        user = models_user.User.objects.create(**self.data)
        self.company.users.add(user)
        self.company.save()
        self.client.post(path=self.endpoint, data=self.data)
        users_quantity = models_user.User.objects.count()
        self.assertEqual(users_quantity, 1)
