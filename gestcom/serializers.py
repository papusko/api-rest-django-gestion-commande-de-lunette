from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import *




class ClientsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Clients
        fields = ('nom', 'prenom', 'adresse', 'telephone','photo')




class LunetteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Lunette
        fields = ('types','photo')



class CommandeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commandes
        fields = ('date_add', 'clients', 'lunette')


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")


class UserRegisterSerializer(serializers.ModelSerializer):    
	
    username = serializers.CharField()
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)
    confirmPassword = serializers.CharField(min_length=8, write_only=True)
    prenom = serializers.CharField()
    nom = serializers.CharField()


    class Meta:
        model = User
        fields = ('prenom','nom','username', 'email', 'password','confirmPassword')


