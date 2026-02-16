from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import FreelancerProfile
from jobs.models import JobApplication, Job

User = get_user_model()


# ---------------- LOGIN ----------------
class EmailAuthForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

    def clean_username(self):
        return self.cleaned_data["username"].lower()


# ---------------- RECRUITER REGISTER ----------------
class RecruiterRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password", "company_name"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please login instead.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        user.user_type = "recruiter"
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


# ---------------- FREELANCER REGISTER ----------------
class FreelancerRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password", "name"]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered. Please login instead.")

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email.lower()
        user.user_type = "freelancer"
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


# ---------------- FREELANCER PROFILE ----------------
class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = [
            "education",
            "experience",
            "skills",
            "tech_stack",
            "bio",
            "hourly_rate",
            "resume",
        ]


# ---------------- JOB POST ----------------
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "description",
            "required_skills",
            "tech_stack",
            "pay_per_hour",
            "experience_level",
        ]


# ---------------- APPLY ----------------
class ApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["cover_letter"]