from django.shortcuts import render,redirect
from django.conf import settings
from rest_framework import viewsets
from rest_framework.views import APIView
from account.models import User,UserBankAccount
from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate,login,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
#for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.authtoken.models import Token


class UserRegistrationView(APIView):
    serializer_class = UserSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data) 
        
        if serializer.is_valid():
            user = serializer.save()
            token=default_token_generator.make_token(user)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link=f'https://rent-vista-7tlr.onrender.com/api/auth/active/{uid}/{token}/'
            # confirm_link=f'http://127.0.0.1:8000/api/auth/active/{uid}/{token}/'
            email_subject='Confirm Your Email'
            email_body=render_to_string('confirm_email.html',{'confirm_link':confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
             # Create UserBankAccount with account number as 
            account_no = user.id + 10000
            UserBankAccount.objects.create(user=user, account_no=account_no)
            return Response(f'Check your mail confirmation your account number {account_no}')
        return Response(serializer.errors)

def activate(request, uid64, token):
    try: 
        uid = urlsafe_base64_decode(uid64).decode() 
        user=get_user_model().objects.get(pk=uid) 
    except get_user_model().DoesNotExist:
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect(settings.LOGIN_URL)
    else:
        return redirect('register')
  
class UserLoginView(APIView):
  def post(self, request):
    serializer = UserLoginSerializer(data = self.request.data)
    if serializer.is_valid():
      username = serializer.validated_data['username']
      password = serializer.validated_data['password']

      user = authenticate(username= username, password=password)
            
      if user:
         token, _ = Token.objects.get_or_create(user=user)
         login(request,user)
         return Response({'token' : token.key, 'user_id' : user.id})
      else:
        return Response({'error' : "username and password incorrect"})
    return Response(serializer.errors)
  


class UserLogoutView(APIView):
#   authentication_classes = [TokenAuthentication]
#   permission_classes = [IsAuthenticated]
  def get(self, request):
    print("user",request.user)
    request.user.auth_token.delete()
    logout(request)
    return redirect(settings.LOGIN_URL)
  
