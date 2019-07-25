from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import TokenSerializer, UserSerializer, UserRegisterSerializer
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings
from django.core.validators import validate_email
from rest_framework import viewsets


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


        lookup_field= 'email'
        lookup_url_kwargs = 'email'
        lookup_value_regex = '[\w@.]+'

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
            username=username, password=password, email=email
        )
        return Response(status=status.HTTP_201_CREATED)



class UserViewSet(viewsets.ModelViewSet):
	
	queryset = User.objects.all()
	serializer_class = UserSerializer

# Create your views here.
