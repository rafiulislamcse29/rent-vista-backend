from account.models import User,UserBankAccount
from rest_framework import viewsets,status
from . import serializers
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
class UserBankAccountViewSet(viewsets.ModelViewSet):
    queryset = UserBankAccount.objects.all()
    serializer_class =serializers.UserBankAccountSerializer

    def get_queryset(self):
        queryset = UserBankAccount.objects.all()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @action(detail=False, methods=['post'])
    def deposit(self, request):
        # account_no = request.data.get('account_no')
        user_id = self.request.query_params.get('user_id')
        balance = request.data.get('balance')
       
        # if account_no is None:
        #     return Response({"error": "Account number incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        if user_id is None:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)


        if balance is None:
            return Response({"error": "balance is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            balance = int(balance)
        except ValueError:
            return Response({"error": "Invalid balance format"}, status=status.HTTP_400_BAD_REQUEST)

        if balance <= 0:
            return Response({"error": "Deposit balance must be greater than zero"}, status=status.HTTP_400_BAD_REQUEST)

       
        try:
            account = UserBankAccount.objects.get(user_id=user_id)
        except UserBankAccount.DoesNotExist:
            return Response({"error": "User Bank Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

       
        account.balance += balance
        account.save()

        return Response({"message": "Deposit successful", "new_balance": account.balance}, status=status.HTTP_200_OK)