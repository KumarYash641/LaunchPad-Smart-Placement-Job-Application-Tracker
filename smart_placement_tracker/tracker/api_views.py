from rest_framework import generics, permissions
from django.db.models import Q
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer


class JobListAPI(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).select_related("company")
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(company__name__icontains=search)
            )
        return queryset


class MyApplicationsAPI(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).select_related("job", "job__company")
