from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ("Housing", "Housing"),
        ("Transportation", "Transportation"),
        ("Dine Out", "Dine Out"),
        ("Healthcare", "Healthcare"),
        ("Entertainment", "Entertainment"),
        ("Shopping", "Shopping"),
        ("Other", "Other"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    title = models.CharField(max_length=120)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="Other")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

class MonthlyBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="monthly_budgets")
    month = models.DateField(help_text="Use the first day of the month")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "month"], name="unique_user_month_budget")
        ]
        ordering = ["-month"]

    def __str__(self):
        return f"{self.user.username} - {self.month:%B %Y}"
