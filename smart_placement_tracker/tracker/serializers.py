from rest_framework import serializers
from .models import Job, Application


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = Job
        fields = [
            "id", "title", "company", "company_name", "description", "location",
            "employment_type", "min_cgpa", "required_skills", "deadline", "is_active",
        ]


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source="job.title", read_only=True)
    company_name = serializers.CharField(source="job.company.name", read_only=True)
    student_username = serializers.CharField(source="student.username", read_only=True)

    class Meta:
        model = Application
        fields = ["id", "student", "student_username", "job", "job_title", "company_name", "status", "applied_at"]
        read_only_fields = ["student", "status", "applied_at"]
