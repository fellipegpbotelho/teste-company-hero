from django.urls import path

from .views.company_views import CreateCompanyView
from .views.user_views import CreateCompanyUserView

app_name = "api"

urlpatterns = [
    path("companies/", CreateCompanyView.as_view(), name="company.create"),
    path(
        "companies/<int:company_id>/users/",
        CreateCompanyUserView.as_view(),
        name="company.user.create",
    )
]
