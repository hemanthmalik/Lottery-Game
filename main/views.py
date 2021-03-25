from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from . import models as main_models
from django.core.exceptions import ValidationError
# from django.contrib.auth.models import User
# Create your views here.

# def user_register():
#     return Response()

User = get_user_model()

@api_view(['POST'])
@parser_classes((JSONParser,))
def register(request):
    response = {'success': False, 'detail': 'Please, provide requested credentials!'}

    data = request.data
    name = data.get('name')
    phone = data.pop('phone')
    email = data.get('email')
    password = data.pop('password')

    if name and phone and password:
        try:
            User.objects.create_user(phone, password, **data)
        except ValidationError as e:
            return Response({'success':False, 'detail': e})
        response = {'success': True, 'detail': 'Registration Successful.'}
    
    return Response(response)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.pk,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'token': token.key,
        })

    
class ValidateAddMoney(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        ref_number = data.get('ref_number')
        amount = data.get('amount')
        main_models.AddedAmount.objects.create(amount=amount, reference_number=ref_number, user=request.user)
        return Response({'success': True, 'detail': 'Payment validation in progress!'})

class PlaceBet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        bet_amount = data.get('bet_amount')
        if request.user.balance < bet_amount:
            return Response({'success': False, 'detail': 'Insufficient Balance!'})
        bet_digit = data.get('bet_digit')
        main_models.Bet.objects.create(amount=bet_amount, number=bet_digit, user=request.user)
        return Response({'success': True, 'detail': 'Bet has been placed!'})