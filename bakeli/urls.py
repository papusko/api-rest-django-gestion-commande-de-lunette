"""bakeli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers
from gestcom.views import UserViewSet
from gestcom.views import *




router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router = routers.DefaultRouter()
router.register(r'clients', ClientsViewSet)
router.register(r'lunette', LunetteViewSet)
router.register(r'commande', CommandeViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('api/',include('gestcom.urls')),
    url(r'^api/', include(router.urls)),
]

