from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ManageCash.urls')),  # This hooks up your dashboard, login, and registration pages
]
