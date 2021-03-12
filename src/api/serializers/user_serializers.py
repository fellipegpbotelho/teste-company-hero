from typing import Any, Dict

from rest_framework import serializers, exceptions

from companies.models import Company
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    company_id = serializers.PrimaryKeyRelatedField(read_only=True)
    email = serializers.EmailField(validators=None)

    class Meta:
        model = User
        fields = ["id", "name", "email", "company_id"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        try:
            company_id = self.context.get("company_id")
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            raise exceptions.ValidationError(
                detail="Company not found.",
                code="400",
            )

        defaults = {
            "company": company_id,
            "name": validated_data.get("name"),
        }
        parameters = {
            "email": validated_data.get("email"),
            "defaults": defaults,
        }
        user, created = User.objects.update_or_create(**parameters)
        if created:
            company.users.add(user)
            company.save()

        return user
