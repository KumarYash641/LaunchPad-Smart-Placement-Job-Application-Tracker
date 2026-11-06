from django.contrib import admin
from .models import StudentProfile, Company, Job, Application


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "college", "cgpa", "graduation_year")
    search_fields = ("full_name", "user__username", "college")
    list_filter = ("graduation_year",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "website")
    search_fields = ("name", "location")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "min_cgpa", "deadline", "is_active")
    list_filter = ("is_active", "employment_type", "company")
    search_fields = ("title", "company__name", "required_skills")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "job", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("student__username", "job__title", "job__company__name")
