from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import Plan, UserSubscription
from .serializers import (
    PlanSerializer,
    UserSerializer,
    UserSubscriptionCreateSerializer,
    UserSubscriptionDetailSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken


# SIGNUP API
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        name = request.data.get("name")
        password = request.data.get("password")

        if not (username and email and password):
            return Response({"error": "username, email, password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken"}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        return Response({"message": "User created successfully"}, status=201)

# LOGIN API (JWT)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

# PLAN LIST API
class PlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = Plan.objects.all()
        ser = PlanSerializer(plans, many=True)
        return Response(ser.data)

# PLAN DETAIL 
class PlanDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plan_id = request.query_params.get("id")

        if not plan_id:
            return Response({"error": "id query parameter is required"}, status=400)

        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=404)

        serializer = PlanSerializer(plan)
        return Response(serializer.data)

# SUBSCRIBE API (POST)
class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ser = UserSubscriptionCreateSerializer(data=request.data)
        if not ser.is_valid():
            return Response(ser.errors, status=400)

        plan = ser.validated_data["plan"]

        start = timezone.now()
        end = start + timedelta(days=plan.duration_days)

        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start,
            end_date=end,
            status="pending"
        )

        out = UserSubscriptionDetailSerializer(subscription)
        return Response(out.data, status=201)

# CURRENT SUBSCRIPTION API
class CurrentSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subs = UserSubscription.objects.filter(user=request.user).order_by("-created_at")

        if not subs.exists():
            return Response({"detail": "No subscription found"}, status=200)


        # Expiry check
        for sub in subs:
            if sub.status == "active" and sub.end_date < timezone.now():
                sub.status = "expired"
                sub.save(update_fields=["status"])

        return Response(UserSubscriptionDetailSerializer(subs, many=True).data)

# WEBHOOK SIMULATION (NO AUTH)
class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("user_email")
        plan_id = request.data.get("plan_id")

        if not (email and plan_id):
            return Response({"error": "user_email and plan_id required"}, status=400)

        user = User.objects.filter(email=email).first()
        plan = Plan.objects.filter(id=plan_id).first()

        if not user or not plan:
            return Response({"error": "Invalid user or plan"}, status=400)

        # Find pending subscription
        pending_sub = UserSubscription.objects.filter(
            user=user,
            plan=plan,
            status="pending"
        ).order_by("-created_at").first()

        if not pending_sub:
            return Response({"error": "No pending subscription found"}, status=404)

        # ACTIVATE subscription
        pending_sub.status = "active"
        pending_sub.start_date = timezone.now()
        pending_sub.end_date = pending_sub.start_date + timedelta(days=plan.duration_days)
        pending_sub.save()

        return Response({
            "message": "Subscription activated",
            "subscription": UserSubscriptionDetailSerializer(pending_sub).data
        })

# ADMIN — ALL USERS + SUBS
class UsersWithSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # SUPERUSER CHECK
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers are allowed to access this endpoint."},
                status=403
            )
        users = User.objects.all()
        output = []

        for user in users:
            latest = user.subscriptions.order_by("-created_at").first()

            if latest:
                if latest.status == "active" and latest.end_date < timezone.now():
                    latest.status = "expired"
                    latest.save(update_fields=["status"])

                latest_ser = UserSubscriptionDetailSerializer(latest).data
            else:
                latest_ser = None

            output.append({
                "user": UserSerializer(user).data,
                "subscription": latest_ser
            })

        return Response(output)

# ADMIN — EXPIRED SUBSCRIPTIONS
class ExpiredSubscriptionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # SUPERUSER CHECK
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers are allowed to access this endpoint."},
                status=403
            )
        
        expired = UserSubscription.objects.filter(status="expired")
        ser = UserSubscriptionDetailSerializer(expired, many=True)
        return Response(ser.data)












