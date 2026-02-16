from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    USER_TYPE_CHOICES = (
        ("freelancer", "Freelancer"),
        ("recruiter", "Recruiter"),
    )

    username = None   # remove username completely

    email = models.EmailField(unique=True)

    name = models.CharField(max_length=200, blank=True)

    company_name = models.CharField(max_length=200, blank=True)

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email