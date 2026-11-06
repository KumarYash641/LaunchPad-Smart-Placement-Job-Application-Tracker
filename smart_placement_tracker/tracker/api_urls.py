from django.urls import path
from .api_views import JobListAPI, MyApplicationsAPI

urlpatterns = [
    path("jobs/", JobListAPI.as_view(), name="api_jobs"),
    path("my-applications/", MyApplicationsAPI.as_view(), name="api_my_applications"),
]
