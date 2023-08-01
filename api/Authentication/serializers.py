from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import VoterOTP
from Student_Register.models import Student_Register

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id','username','email','first_name','last_name','password') 
        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('id', 'username', 'email','first_name','last_name','password')
        extra_kwargs = {
                       'password': {'write_only':True},
                       'first_name':{'required':True},
                       'last_name':{'required':True},
                       
                       }

    def create(self, validated_data):
        try:
            user = User.objects.create_user(username=validated_data['username'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'],
                                            email=validated_data['email'],
                                            password=validated_data['password'])
            return user
        except KeyError as e:
            return e

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField() 
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Incorect credentials Passed')

class VoterIdSerializer(serializers.Serializer):
    voter_id = serializers.CharField()

    def validate(self, data):
        try:
            voter = Student_Register.objects.get(voter_id=data['voter_id'])
        
            return voter
        except Student_Register.DoesNotExist:
            return serializers.ValidationError('Incorect credentials Passed')


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['username']

        
class VoterOTPSerializer(serializers.ModelSerializer):
    voter = serializers.CharField(max_length=20)
    otp = serializers.CharField(max_length=20)
    class Meta:
        model = VoterOTP 
        fields = ['voter','otp', 'used']
        extra_kwargs = {
            'used':{'read_only':True},
           
        }

    

    # def validate(self, data):
        
    #     try:
    #         voter = VoterOTP.objects.get(voter__voter_id=data['voter'],otp=data['otp'])
          

    #         if voter:
    #             voter.used = True 
    #             voter.save()
    #             return voter
    #         else:
    #             return False
    #     except VoterOTP.DoesNotExist:
            
    #         return None