from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserCreationForm, Custo

# Register your models here.

admin.site.register(Clients)
admin.site.register(Lunette)
admin.site.register(Commandes)
