from django.urls import path
from .serializers import *
from .views import LoginView, RegisterUsers, UserViewSet
from .models import *




urlpatterns = [
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
    ]