from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serialilizers import TransactionSerializer, WalletSerializer

from decimal import Decimal
from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings
import requests
import uuid

# Create your views here.


class WalletCreateView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user
        # first_name = data['firstname']
        # last_name = data['lastnaem']
        wallet = Wallet.objects.create(user=user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
    
# class DepositFunds(APIView):

#     def post(self, request):
#         serializer = DepositSerializer(
#             data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)

#         resp = serializer.save()
#         return Response(resp)    

class DepositeView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        transaction_type = data['transaction_type']
        user = self.request.user
        amount = data['amount']
        balance = user.balance
        balance_after = balance + Decimal(amount)
        user.balance = balance_after
        response = requests.post('https://api.paystack.co/transaction/initialize', headers={
            'Authorization': f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            'Content-Type': 'application/json'
        },
             json={
            'amount': amount,
            'email': user.email,
            'callback_url': 'http://localhost:8000/callback'
        })
        resp = response.json()
        deposite = Deposite.objects.create(
            user=user,
            amount=amount   
        )
        transaction = Transaction.objects.create(user=user, amount=amount,
                                                 balance_before=balance, 
                                                 balance_after=balance_after, 
                                                 transaction_type=transaction_type,
                                                 paystack_payment_reference = resp['data']['reference'],
                                                #  paystack_payment_reference = str(uuid.uuid4)[0:7]
                                                 
                                                 )
        user.save()
        deposite.save()
        transaction.save()
        serializer = TransactionSerializer(transaction)
        return Response({'authorization_url': resp['data']['authorization_url']})
        
        
        response = r.json()
        print(response['data'])
        # print("balance before: ", balance)
        # print("new balance: ", balance_after)
        # return Response({"success": serializer.data})
        return Response({'authorization_url': response['data']['authorization_url']})
    
class VerifyDepositeView(APIView):
    def get(self, request, reference):
        transaction = Transaction.objects.get(
            paystack_payment_reference=reference, user=self.request.user)
        reference = transaction.paystack_payment_reference
        url = 'https://api.paystack.co/transaction/verify/{}'.format(reference)
        headers = {
            {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
        }
        r = request.get(url, headers=headers)
        resp = r.json()
        if resp['data']['status'] == 'success':
            status = resp['data']['status']
            amount = resp['data']['amount']
            transaction.objects.filter(paystack_payment_reference=reference).update(status=status,
                                                                                        amount=amount)
            return Response(resp)
        return Response(resp)
    
    
class WithdrawView(APIView):
    def post(self, request, format=None):
        # transaction_type = "Withdraw"
        data = self.request.data
        user = self.request.user
        amount = data['amount']
        transaction_type = data["transaction_type"]
        balance = user.balance
        if balance < amount:
            return Response({"error:":"Insufficient Balance"})
        else:
            
            balance_after = balance - Decimal(amount)
            user.balance = balance_after
            user.save()
            print("balance before: ", balance)
            print("new balance: ", balance_after)
            withdraw = Withdraw.objects.create(
                user=user,
                amount=amount   
            )
            withdraw.save()
            transaction = Transaction.objects.create(user=user, amount=amount, balance_before=balance, balance_after=balance_after, transaction_type=transaction_type)
            transaction.save()
            serializer = TransactionSerializer(transaction)
            return Response({"success": serializer.data})
            
class TransferView(APIView):
    def post(self, request, format=None):
        # transaction_type = "Withdraw"
        user = self.request.user
        data = self.request.data
        id = data['user_id']
        sent_to = User.objects.get(id=id)
        amount = data['amount']
        transaction_type = data["transaction_type"]
        balance = user.balance
        if balance < amount:
            return Response({"error:":"Insufficient Balance"})
        else:
            
            balance_after = balance - Decimal(amount)
            user.balance = balance_after
            sent_to.balance = sent_to.balance + Decimal(amount)
            sent_to.save()
            user.save()
            print("balance before: ", balance)
            print("new balance: ", balance_after)
            transfer = Transfer.objects.create(
                user=user,
                amount=amount,
                sent_to = sent_to.name   
            )
            transfer.save()
            transaction = Transaction.objects.create(user=user, amount=amount, sent_to = sent_to.name, balance_before=balance, balance_after=balance_after, transaction_type=transaction_type, status="success")
            transaction.save()
            serializer = TransactionSerializer(transaction)
            return Response({"success": serializer.data})
        
        
class WalletTransaction(APIView):
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user
        amount = data['amount']
        # wallet = data['wallet']
        transaction_type = data['transaction_type'] 
        wallet = Wallet.objects.all()
        print(wallet)
        print(user.id)
        return Response("ok")
        
       
        