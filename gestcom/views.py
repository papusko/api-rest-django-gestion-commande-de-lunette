from django.shortcuts import render
from rest_framework.renderers import JSONRenderer
from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from django.core.validators import validate_email
from rest_framework import viewsets
from .models import Clients
from django.db import models
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Add this view to your views.py file

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()


    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# Add these lines to the views.py file
class RegisterUsers(generics.CreateAPIView):
    """
    POST auth/register/
    """
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        prenom = request.data.get("prenom", "")
        nom = request.data.get("nom", "")
        confirmPassword = request.data.get("confirmPassword", "")


        

        #verification des champs tout les champs sont obligatoire
        if not username or not password or not email or not prenom or not nom or not confirmPassword:
            return Response(
                data={
                    "message": "Tout les champs sont obligatoire pour votre inscription"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        #verification du mot et de la confirmation s'ils sont identique
        elif password != confirmPassword:
            return Response(
                data={
                    "message": "mot de passe et confirmPassword ne sont pas identiques"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        #verification de la taille du champs password
        elif len(password) < 8 :
            return Response(
                data={
                    "message": "mot de passe trop court le mot de passe doit contenir au moins 8 carractères"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            prenom =prenom, nom=nom, username=username, password=password, email=email
        )
        new_user.save()
        return new_user
        return Response(status=status.HTTP_201_CREATED)



class UserViewSet(viewsets.ModelViewSet):
    	
	queryset = User.objects.all()
	serializer_class = UserSerializer



class ClientsView(generics.CreateAPIView):


    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        serializer = ClientsSerializer()
        return Response({'serializer': serializer})




class ClientsViewSet(viewsets.ModelViewSet):

    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    permission_classes = (permissions.AllowAny,)




class LunetteViewSet(viewsets.ModelViewSet):

    queryset = Lunette.objects.all()
    serializer_class = LunetteSerializer
    permission_classes = (permissions.AllowAny,)


class CommandeViewSet(viewsets.ModelViewSet):

    queryset = Commandes.objects.all()
    serializer_class = CommandeSerializer
    permission_classes = (permissions.AllowAny,)

