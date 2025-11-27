from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Subscription Plans
class Plan(models.Model):
    name = models.CharField(max_length=50)  # Basic / Pro / Enterprise
    price = models.DecimalField(max_digits=8, decimal_places=2)  # ₹199 / 399 / 999
    duration_days = models.PositiveIntegerField()  # usually 30 days

    def __str__(self):
        return f"{self.name} - ₹{self.price}"
    

# User Subscription
class UserSubscription(models.Model):
    STATUS_CHOICES = (
        ("active", "Active"),
        ("expired", "Expired"),
        ("pending", "Pending")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)

    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # auto-calculate end date only on create
        if not self.end_date:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    def check_and_update_expiry(self):
        if self.status == "active" and self.end_date < timezone.now():
            self.status = "expired"
            self.save(update_fields=["status"])

    def __str__(self):
        return f"{self.user.username} -> {self.plan.name} ({self.status})"
