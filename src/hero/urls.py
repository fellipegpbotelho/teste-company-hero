from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="api/companies/", permanent=True)),
    path("api/", include("api.urls"), name="api"),
    path("api-auth/", include("rest_framework.urls")),
]
