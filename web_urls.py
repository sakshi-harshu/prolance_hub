from django.urls import path
from . import web_views

urlpatterns = [
    path("", web_views.home, name="home"),

    path("login/", web_views.login_view, name="login"),
    path("logout/", web_views.logout_view, name="logout"),

    path("register/recruiter/", web_views.register_recruiter, name="register_recruiter"),
    path("register/freelancer/", web_views.register_freelancer, name="register_freelancer"),

    path("recruiter-dashboard/", web_views.recruiter_dashboard, name="recruiter_dashboard"),
    path("freelancer-dashboard/", web_views.freelancer_dashboard, name="freelancer_dashboard"),

    path("freelancer/profile/", web_views.freelancer_profile_create, name="freelancer_profile_create"),

    path("jobs/post/", web_views.post_job, name="post_job"),
    path("jobs/<int:job_id>/apply/", web_views.apply_job, name="apply_job"),

    path("applications/<int:app_id>/accept/", web_views.accept_application, name="accept_application"),
    path("applications/<int:app_id>/reject/", web_views.reject_application, name="reject_application"),
]