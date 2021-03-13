from django.urls import path

from .views.company_views import CreateCompanyView, GetCompanyView
from .views.user_views import CreateCompanyUserView, GetUserView

app_name = "api"

urlpatterns = [
    path(
        route="companies/",
        view=CreateCompanyView.as_view(),
        name="company.create",
    ),
    path(
        route="companies/<int:id>/",
        view=GetCompanyView.as_view(),
        name="company.show",
    ),
    path(
        route="companies/<int:id>/users/",
        view=CreateCompanyUserView.as_view(),
        name="company.user.create",
    ),
    path(
        route="users/",
        view=GetUserView.as_view(),
        name="user.show",
    )
]
