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
# from django.contrib.auth.models import User
# Create your views here.

# def user_register():
#     return Response()

User = get_user_model()

@api_view(['POST'])
@parser_classes((JSONParser,))
def register(request):
    response = {'success': False, 'detail': 'Please, provide all credentials!'}

    data = request.data
    name = data.get('name')
    phone = data.get('phone')
    email = data.pop('email')
    password = data.pop('password')

    if name and phone and email and password:
        User.objects.create_user(email, password, **data)
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
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

    
class ValidateAddMoney(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        data = request.data
        main_models.AddedMoney.objects.create(amount=data.get('amount'), reference_number=data.get('ref_number'), user=request.user)
        return Response({'success': True, 'detail': 'Money sent for validation!'})