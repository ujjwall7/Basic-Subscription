from django.urls import path
from .views import *


urlpatterns = [

    # Auth
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", LoginView.as_view(), name="login"),

    # Plans
    path("plans/", PlanListView.as_view(), name="plans-list"),
    path("plans/detail/", PlanDetailView.as_view(), name="plan-detail"),

    # Subscription
    path("subscription/", SubscribeView.as_view(), name="subscribe"),
    path("subscription/current/", CurrentSubscriptionView.as_view(), name="current-subscription"),

    # Webhook simulation
    path("webhook/payment-success/", PaymentWebhookView.as_view(), name="payment-webhook"),

    # Admin/Dashboard (SUPERUSER ONLY)
    path("users-with-subscription/", UsersWithSubscriptionView.as_view(), name="users-with-subscription"),
    path("expired-subscriptions/", ExpiredSubscriptionsView.as_view(), name="expired-subscriptions"),
]
