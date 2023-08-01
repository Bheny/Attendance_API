from drf_base64.fields import Base64ImageField
from rest_framework import serializers

from .models import Student_Register
# from Votes.serializers import VoteSerializer

class StudentRegisterSerializer(serializers.ModelSerializer):
    photo = Base64ImageField()
    casted_ballots = serializers.SerializerMethodField()
    class Meta:
        model = Student_Register
        fields = "__all__"
        extra_kwargs = {
            'is_verified':{'read_only':True},
            'verified_by':{'read_only':True},
        }
    


class VerifyVoterSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(required=True)
    photo = Base64ImageField(required=True)
    
    class Meta:
        model = Student_Register
        fields = "__all__"
    
    
    def create(self, validated_data):
        return validated_data
        # return Register.objects.create(**validated_data)
