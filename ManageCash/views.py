from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import AddCash, Expense

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

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
            
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cash_data = AddCash.objects.filter(user=request.user).aggregate(Sum('amount'))
    total_cash = cash_data['amount__sum'] or 0
    
    expense_data = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))
    total_expense = expense_data['amount__sum'] or 0
    
    balance = total_cash - total_expense
    
    context = {
        'total_cash': total_cash,
        'total_expense': total_expense,
        'balance': balance,
    }
    return render(request, 'dashboard.html', context)

def add_cash_view(request):
    if request.method == 'POST':
        s = request.POST.get('source')
        a = request.POST.get('amount')
        d = request.POST.get('description')
        
        AddCash.objects.create(user=request.user, source=s, amount=a, description=d)
        return redirect('dashboard')
        
    return redirect('dashboard')

def add_expense_view(request):
    if request.method == 'POST':
        a = request.POST.get('amount')
        d = request.POST.get('description')
        
        Expense.objects.create(user=request.user, amount=a, description=d)
        return redirect('dashboard')
        
    return redirect('dashboard')
