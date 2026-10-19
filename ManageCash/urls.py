from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-cash/', views.add_cash_view, name='add_cash'),
    path('add-expense/', views.add_expense_view, name='add_expense'),
]
