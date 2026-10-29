
from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from expenses.models import Expense, MonthlyBudget


class Command(BaseCommand):
    help = "Create demo expenses and a monthly budget"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="demo",
            defaults={"email": "demo@example.com"},
        )

        if created:
            user.set_password("maha@2K5")
            user.save()

        MonthlyBudget.objects.update_or_create(
            user=user,
            month=date(2023, 6, 1),
            defaults={"amount": Decimal("3500.00")},
        )

        demo_expenses = [
            ("Groceries", "Dine Out", "1500.00"),
            ("Bus and travel", "Transportation", "800.00"),
            ("Daily shopping", "Shopping", "1000.00"),
            ("Movie", "Entertainment", "700.00"),
        ]

        for title, category, amount in demo_expenses:
            Expense.objects.get_or_create(
                user=user,
                title=title,
                date=date(2023, 6, 15),
                defaults={
                    "category": category,
                    "amount": Decimal(amount),
                    "notes": "Sample dashboard expense",
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data created. Username: demo | Password: DemoPass123!"
            )
        )
