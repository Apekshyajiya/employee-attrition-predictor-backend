from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','name','username','password','password','email','age','years_of_exp','profile_pic']
        extra_kwargs = {'password': {'write_only':True}}
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass