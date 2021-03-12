from django.urls import path

from .views.company_views import CreateCompanyView

app_name = "api"

urlpatterns = [
    path("companies/", CreateCompanyView.as_view(), name="company.create")
]
