from django.urls import path
from django.shortcuts import redirect
from .views import *  # Importa tudo do arquivo views.py

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('', lambda request: redirect('login')),  # Redireciona para 'login' quando a URL estiver vazia
]
