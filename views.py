from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Skill, TechStack, FreelancerProfile
from .serializers import (
    UserRegisterSerializer,
    SkillSerializer,
    TechStackSerializer,
    FreelancerProfileSerializer,
)
from common.permissions import IsFreelancer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all().order_by("name")
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]


class TechStackViewSet(viewsets.ModelViewSet):
    queryset = TechStack.objects.all().order_by("name")
    serializer_class = TechStackSerializer
    permission_classes = [IsAuthenticated]


class FreelancerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = FreelancerProfileSerializer
    permission_classes = [IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        return FreelancerProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)