from django.urls import include, path

urlpatterns = [
    path("api/", include("api.urls"), name="api"),
    path("api-auth/", include("rest_framework.urls")),
]
