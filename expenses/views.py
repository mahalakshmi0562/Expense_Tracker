from datetime import date
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, MonthlyBudget

@login_required
def dashboard(request):
    today = date.today()
    month_start = today.replace(day=1)
    if request.method == "POST" and request.POST.get("action") == "set_budget":
        try:
            budget_amount = Decimal(request.POST.get("budget_amount", "0"))
            if budget_amount <= 0:
                raise ValueError
            MonthlyBudget.objects.update_or_create(
                user=request.user, month=month_start, defaults={"amount": budget_amount}
            )
            messages.success(request, "Monthly budget updated.")
        except (ValueError, ArithmeticError):
            messages.error(request, "Enter a budget amount greater than zero.")
        return redirect("dashboard")
    expenses = Expense.objects.filter(user=request.user, date__year=today.year, date__month=today.month)
    total = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    budget_obj = MonthlyBudget.objects.filter(user=request.user, month=month_start).first()
    budget = budget_obj.amount if budget_obj else Decimal("0.00")
    remaining = budget - total

    category_totals = list(
        expenses.values("category").annotate(total=Sum("amount")).order_by("-total")
    )
    monthly_totals = []
    for month in range(1, 13):
        amount = Expense.objects.filter(
            user=request.user, date__year=today.year, date__month=month
        ).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
        monthly_totals.append(float(amount))

    recent_expenses = expenses[:6]
    context = {
        "today": today, "total": total, "budget": budget, "remaining": remaining,
        "category_totals": category_totals, "monthly_totals": monthly_totals,
        "recent_expenses": recent_expenses,
        "expense_count": expenses.count(),
    }
    return render(request, "expenses/dashboard.html", context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "expenses/register.html", {"form": form})

@login_required
def add_expense(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "Other")
        amount = request.POST.get("amount", "0")
        expense_date = request.POST.get("date", "")
        notes = request.POST.get("notes", "").strip()
        try:
            amount_value = Decimal(amount)
            if not title or amount_value <= 0 or not expense_date:
                raise ValueError
            Expense.objects.create(
                user=request.user, title=title, category=category,
                amount=amount_value, date=expense_date, notes=notes
            )
            messages.success(request, "Expense added successfully.")
            return redirect("dashboard")
        except (ValueError, ArithmeticError):
            messages.error(request, "Enter a title, a valid date, and an amount greater than zero.")
    return render(request, "expenses/add_expense.html", {"today": date.today(), "categories": Expense.CATEGORY_CHOICES})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Expense deleted.")
    return redirect("dashboard")
