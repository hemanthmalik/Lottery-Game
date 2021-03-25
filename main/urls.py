from django.urls import path, include
from rest_framework.authtoken import views
from . import views as main_view

urlpatterns = [
    path('register/', main_view.register, name='register'),
    path('login/', main_view.CustomAuthToken.as_view()),
    path('add-money/', main_view.ValidateAddMoney.as_view(), name='add_money'),
    path('place-bet/', main_view.PlaceBet.as_view(), name='place_bet')
]