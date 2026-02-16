from rest_framework import serializers
from .models import User, FreelancerProfile, Skill, TechStack


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ["email", "username", "password", "user_type"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class TechStackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechStack
        fields = ["id", "name"]


class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all(), required=False)
    tech_stack = serializers.PrimaryKeyRelatedField(many=True, queryset=TechStack.objects.all(), required=False)

    class Meta:
        model = FreelancerProfile
        fields = ["id", "education", "experience", "skills", "tech_stack", "bio", "hourly_rate", "resume"]