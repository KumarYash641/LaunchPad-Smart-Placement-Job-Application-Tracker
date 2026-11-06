from django.conf import settings
from django.db import models
from django.utils import timezone


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile"
    )
    full_name = models.CharField(max_length=120)
    college = models.CharField(max_length=160, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    graduation_year = models.PositiveSmallIntegerField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    skills = models.CharField(
        max_length=500, blank=True,
        help_text="Enter comma-separated skills, e.g. Python, SQL, HTML"
    )
    resume_link = models.URLField(blank=True)

    def skill_list(self):
        return [skill.strip().lower() for skill in self.skills.split(",") if skill.strip()]

    def __str__(self):
        return self.full_name


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    description = models.TextField()
    location = models.CharField(max_length=120, blank=True)
    employment_type = models.CharField(
        max_length=30,
        choices=[("Full-time", "Full-time"), ("Internship", "Internship"), ("Contract", "Contract")],
        default="Full-time",
    )
    min_cgpa = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    required_skills = models.CharField(
        max_length=500, blank=True,
        help_text="Comma-separated skills, e.g. Python, SQL"
    )
    deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def required_skill_list(self):
        return [skill.strip().lower() for skill in self.required_skills.split(",") if skill.strip()]

    def is_open(self):
        return self.is_active and (self.deadline is None or self.deadline >= timezone.localdate())

    def __str__(self):
        return f"{self.title} - {self.company.name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ("Applied", "Applied"),
        ("Under Review", "Under Review"),
        ("Shortlisted", "Shortlisted"),
        ("Rejected", "Rejected"),
        ("Selected", "Selected"),
    ]
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Applied")
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-applied_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "job"], name="unique_student_job_application")
        ]

    def __str__(self):
        return f"{self.student.username} - {self.job.title}"
