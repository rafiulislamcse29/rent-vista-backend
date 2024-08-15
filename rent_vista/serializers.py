
from rest_framework import serializers
from account.models import User,UserBankAccount

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name', 'last_name', 'email','role']

class UserBankAccountSerializer(serializers.ModelSerializer):
   class Meta:
    model=UserBankAccount
    fields='__all__'
