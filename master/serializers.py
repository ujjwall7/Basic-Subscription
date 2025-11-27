from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plan, UserSubscription


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ("id", "name", "price", "duration_days")


# POST — Create Subscription
class UserSubscriptionCreateSerializer(serializers.ModelSerializer):
    plan_id = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all(),
        source="plan",
        write_only=True
    )

    class Meta:
        model = UserSubscription
        fields = ("plan_id",)


# GET — Subscription details (nested)
class UserSubscriptionDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = UserSubscription
        fields = (
            "id",
            "user",
            "plan",
            "start_date",
            "end_date",
            "status",
            "created_at",
        )
