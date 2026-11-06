from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import RegisterForm, ProfileForm
from .models import Application, Job, StudentProfile
from .services import check_eligibility


def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard_view(request):
    applications = Application.objects.filter(student=request.user).select_related("job", "job__company")
    profile = getattr(request.user, "student_profile", None)
    stats = {
        "total": applications.count(),
        "shortlisted": applications.filter(status="Shortlisted").count(),
        "selected": applications.filter(status="Selected").count(),
        "rejected": applications.filter(status="Rejected").count(),
    }
    recent_applications = applications[:5]
    recommended_jobs = []
    if profile:
        for job in Job.objects.filter(is_active=True).select_related("company")[:30]:
            eligible, reasons = check_eligibility(profile, job)
            if eligible:
                recommended_jobs.append(job)
    return render(request, "tracker/dashboard.html", {
        "profile": profile, "stats": stats,
        "recent_applications": recent_applications,
        "recommended_jobs": recommended_jobs[:5],
    })


@login_required
def profile_view(request):
    profile, _ = StudentProfile.objects.get_or_create(
        user=request.user,
        defaults={"full_name": request.user.get_full_name() or request.user.username},
    )
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
    return render(request, "tracker/profile.html", {"form": form})


@login_required
def job_list_view(request):
    query = request.GET.get("q", "").strip()
    jobs = Job.objects.filter(is_active=True).select_related("company")
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__name__icontains=query) |
            Q(location__icontains=query) |
            Q(required_skills__icontains=query)
        )
    paginator = Paginator(jobs, 8)
    page_obj = paginator.get_page(request.GET.get("page"))
    profile = getattr(request.user, "student_profile", None)
    eligibility = {}
    if profile:
        for job in page_obj:
            eligibility[job.id] = check_eligibility(profile, job)
    return render(request, "tracker/job_list.html", {
        "page_obj": page_obj, "query": query, "eligibility": eligibility
    })


@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(Job.objects.select_related("company"), pk=pk)
    profile = getattr(request.user, "student_profile", None)
    eligible, reasons = check_eligibility(profile, job) if profile else (False, ["Complete your student profile first."])
    already_applied = Application.objects.filter(student=request.user, job=job).exists()
    return render(request, "tracker/job_detail.html", {
        "job": job, "eligible": eligible, "reasons": reasons, "already_applied": already_applied
    })


@login_required
def apply_job_view(request, pk):
    if request.method != "POST":
        return redirect("job_detail", pk=pk)
    job = get_object_or_404(Job, pk=pk)
    profile = getattr(request.user, "student_profile", None)
    if not profile:
        messages.error(request, "Student profile not found.")
        return redirect("profile")
    eligible, reasons = check_eligibility(profile, job)
    if not eligible:
        messages.error(request, "You are not eligible: " + " ".join(reasons))
        return redirect("job_detail", pk=pk)
    try:
        Application.objects.create(student=request.user, job=job)
        messages.success(request, "Application submitted successfully.")
    except IntegrityError:
        messages.warning(request, "You have already applied for this job.")
    return redirect("my_applications")


@login_required
def my_applications_view(request):
    applications = Application.objects.filter(student=request.user).select_related("job", "job__company")
    return render(request, "tracker/my_applications.html", {"applications": applications})


@user_passes_test(lambda u: u.is_staff)
def manage_applications_view(request):
    if request.method == "POST":
        application_id = request.POST.get("application_id")
        status = request.POST.get("status")
        valid_statuses = dict(Application.STATUS_CHOICES)
        application = get_object_or_404(Application, pk=application_id)
        if status in valid_statuses:
            application.status = status
            application.save()
            messages.success(request, "Application status updated.")
        return redirect("manage_applications")
    applications = Application.objects.select_related("student", "job", "job__company")
    return render(request, "tracker/manage_applications.html", {
        "applications": applications,
        "status_choices": Application.STATUS_CHOICES,
    })
