from django.urls import path
from .views import *


urlpatterns = [

    # Auth
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/token/", LoginView.as_view(), name="login"),

    # Plans
    path("plans/", PlanListView.as_view(), name="plans-list"),
    path("plans/<int:pk>/", PlanDetailView.as_view(), name="plan-detail"),

    # Subscription
    path("subscribe/", SubscribeView.as_view(), name="subscribe"),
    path("subscription/current/", CurrentSubscriptionView.as_view(), name="current-subscription"),

    # Webhook simulation
    path("webhook/payment-success/", PaymentWebhookView.as_view(), name="payment-webhook"),

    # Admin/Dashboard (SUPERUSER ONLY)
    path("admin/dashboard/users-with-subscription/", UsersWithSubscriptionView.as_view(), name="users-with-subscription"),
    path("admin/dashboard/expired-subscriptions/", ExpiredSubscriptionsView.as_view(), name="expired-subscriptions"),
]
