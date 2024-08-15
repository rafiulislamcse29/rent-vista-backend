from rest_framework import serializers
from .models import User,UserBankAccount

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True) 
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password','role']

    def save(self):
      username = self.validated_data['username']
      first_name = self.validated_data['first_name']
      last_name = self.validated_data['last_name']
      email = self.validated_data['email']
      password = self.validated_data['password']
      password2 = self.validated_data['confirm_password']
      role = self.validated_data['role']
      
      if password != password2:
        raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
      
      if User.objects.filter(email=email).exists():
          raise serializers.ValidationError({'error' : "Email Already exists"})
      
      account = User(username = username, email=email, first_name = first_name, last_name = last_name,role=role)
      account.set_password(password)
      account.is_active=False
      account.save()
      return account

class UserBankAccountSerializer(serializers.ModelSerializer):
   class Meta:
    model=UserBankAccount
    fields='__all__'


class UserLoginSerializer(serializers.Serializer):
  username = serializers.CharField(required = True)
  password = serializers.CharField(required = True)



# class UserProfileSerializer(serializers.Serializer):
#     class Meta:
#       model = User
#       fields = ['username', 'first_name', 'last_name', 'email', 'role'] 
