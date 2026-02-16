from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count

from accounts.models import Skill, TechStack, FreelancerProfile
from jobs.models import Job, JobApplication
from .forms import (
    EmailAuthForm,
    RecruiterRegisterForm,
    FreelancerRegisterForm,
    FreelancerProfileForm,
    JobForm,
    ApplyForm,
)


def home(request):
    if request.user.is_authenticated:
        if request.user.user_type == "recruiter":
            return redirect("recruiter_dashboard")
        return redirect("freelancer_dashboard")
    return render(request, "accounts/home.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = EmailAuthForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        # AuthenticationForm already authenticated user
        login(request, form.get_user())
        return redirect("home")

    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def register_recruiter(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = RecruiterRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register_recruiter.html", {"form": form})


def register_freelancer(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = FreelancerRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "accounts/register_freelancer.html", {"form": form})


@login_required
def freelancer_profile_create(request):
    if request.user.user_type != "freelancer":
        return HttpResponseForbidden("Only freelancers can create profile.")

    profile = getattr(request.user, "freelancer_profile", None)
    if profile:
        # already created; redirect to dashboard
        return redirect("freelancer_dashboard")

    form = FreelancerProfileForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        profile = form.save(commit=False)
        profile.user = request.user
        profile.save()
        form.save_m2m()
        return redirect("freelancer_dashboard")

    return render(request, "accounts/freelancer_profile.html", {"form": form})


@login_required
def recruiter_dashboard(request):
    if request.user.user_type != "recruiter":
        return HttpResponseForbidden("Recruiter only.")

    jobs = (
        Job.objects.filter(recruiter=request.user)
        .annotate(app_count=Count("applications"))
        .order_by("-created_at")
    )
    total_jobs = jobs.count()
    total_applicants = JobApplication.objects.filter(job__recruiter=request.user).count()
    applications = JobApplication.objects.filter(job__recruiter=request.user).select_related("job", "freelancer").order_by("-applied_at")[:20]

    context = {
        "jobs": jobs,
        "total_jobs": total_jobs,
        "total_applicants": total_applicants,
        "applications": applications,
    }
    return render(request, "accounts/recruiter_dashboard.html", context)


@login_required
def freelancer_dashboard(request):
    if request.user.user_type != "freelancer":
        return HttpResponseForbidden("Freelancer only.")

    profile = getattr(request.user, "freelancer_profile", None)
    profile_completion = 20
    if profile:
        # rough completion score
        profile_completion = 60
        if profile.skills.exists(): profile_completion += 10
        if profile.tech_stack.exists(): profile_completion += 10
        if profile.bio.strip(): profile_completion += 10
        if profile.resume: profile_completion += 10
        profile_completion = min(profile_completion, 100)

    jobs = Job.objects.filter(is_active=True).order_by("-created_at")[:20]
    applied_jobs = JobApplication.objects.filter(freelancer=request.user).count()

    context = {
        "profile": profile,
        "profile_completion": profile_completion,
        "jobs": jobs,
        "applied_jobs": applied_jobs,
    }
    return render(request, "accounts/freelancer_dashboard.html", context)


@login_required
def post_job(request):
    if request.user.user_type != "recruiter":
        return HttpResponseForbidden("Recruiter only.")

    form = JobForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.recruiter = request.user
        job.save()
        form.save_m2m()
        return redirect("recruiter_dashboard")

    return render(request, "accounts/post_job.html", {"form": form})


@login_required
def apply_job(request, job_id):
    if request.user.user_type != "freelancer":
        return HttpResponseForbidden("Freelancer only.")

    job = get_object_or_404(Job, id=job_id, is_active=True)
    already = JobApplication.objects.filter(job=job, freelancer=request.user).exists()
    if already:
        return redirect("freelancer_dashboard")

    form = ApplyForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        app = form.save(commit=False)
        app.job = job
        app.freelancer = request.user
        app.status = "applied"
        app.save()
        return redirect("freelancer_dashboard")

    return render(request, "accounts/apply_job.html", {"job": job, "form": form})


@login_required
def accept_application(request, app_id):
    if request.user.user_type != "recruiter":
        return HttpResponseForbidden("Recruiter only.")

    app = get_object_or_404(JobApplication, id=app_id)
    if app.job.recruiter != request.user:
        return HttpResponseForbidden("Not your job.")

    app.status = "accepted"
    app.save()
    return redirect("recruiter_dashboard")


@login_required
def reject_application(request, app_id):
    if request.user.user_type != "recruiter":
        return HttpResponseForbidden("Recruiter only.")

    app = get_object_or_404(JobApplication, id=app_id)
    if app.job.recruiter != request.user:
        return HttpResponseForbidden("Not your job.")

    app.status = "rejected"
    app.save()
    return redirect("recruiter_dashboard")