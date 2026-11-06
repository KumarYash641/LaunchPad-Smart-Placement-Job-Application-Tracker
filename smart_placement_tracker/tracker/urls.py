from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("register/", views.register_view, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("jobs/", views.job_list_view, name="job_list"),
    path("jobs/<int:pk>/", views.job_detail_view, name="job_detail"),
    path("jobs/<int:pk>/apply/", views.apply_job_view, name="apply_job"),
    path("my-applications/", views.my_applications_view, name="my_applications"),
    path("manage-applications/", views.manage_applications_view, name="manage_applications"),
]
