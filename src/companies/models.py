from django.db import models

from users.models import User


class Company(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f"[{self.id}] {self.name}"
