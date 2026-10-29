from django.contrib import admin
from .models import Expense, MonthlyBudget

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "amount", "date")
    list_filter = ("category", "date")
    search_fields = ("title", "user__username")

@admin.register(MonthlyBudget)
class MonthlyBudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "month", "amount")
