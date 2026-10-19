from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import AddCash, Expense

# 1. User Registration View
def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p1 = request.POST.get('password1')
        p2 = request.POST.get('password2')
        
        if p1 == p2:
            user = User.objects.create_user(username=u, password=p1)
            user.save()
            return redirect('login')
            
    return render(request, 'register.html')

# 2. User Login View
def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            
    return render(request, 'login.html')

# 3. User Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# 4. Main Financial Dashboard View
def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch all records belonging to the logged-in user
    user_incomes = AddCash.objects.filter(user=request.user)
    user_expenses = Expense.objects.filter(user=request.user)
    
    # Calculate Total Income (Safe Python Loop to bypass database column bugs)
    total_cash = 0
    for income in user_incomes:
        total_cash += float(getattr(income, 'amount', 0))
    
    # Calculate Total Expenses
    total_expense = 0
    for expense in user_expenses:
        total_expense += float(getattr(expense, 'amount', 0))
    
    # Calculate Remaining Balance
    balance = total_cash - total_expense
    
    # Get the data lists ordered by newest first for the transaction logs
    incomes = user_incomes.order_by('-datetime')
    expenses = user_expenses.order_by('-datetime')
    
    context = {
        'total_cash': total_cash,
        'total_expense': total_expense,
        'balance': balance,
        'incomes': incomes,
        'expenses': expenses,
    }
    return render(request, 'dashboard.html', context)

# 5. Add Cash Form View
def add_cash_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        s = request.POST.get('source')
        a = request.POST.get('amount')
        d = request.POST.get('description')
        
        AddCash.objects.create(user=request.user, source=s, amount=a, description=d)
        return redirect('dashboard')
        
    # Opens a clean separate page showing the source, amount, and description fields
    return render(request, 'transaction_form.html', {'title': 'Add Incoming Cash', 'show_source': True})

# 6. Add Expense Form View
def add_expense_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == 'POST':
        a = request.POST.get('amount')
        d = request.POST.get('description')
        
        Expense.objects.create(user=request.user, amount=a, description=d)
        return redirect('dashboard')
        
    # Opens a clean separate page showing only amount and description fields
    return render(request, 'transaction_form.html', {'title': 'Add Outgoing Expense', 'show_source': False})
