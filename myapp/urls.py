from django.urls import path
from django.shortcuts import redirect
from .views import (download_excel, download_pdf, login_view, registro_view, logout_view, relatorio, 
                    editar_registro, excluir_registro)  # Importa apenas o necessário

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registro/', registro_view, name='registro'),
    path('logout/', logout_view, name='logout'),
    path('relatorio/', relatorio, name='relatorio'),
    path('editar/<int:registro_id>/', editar_registro, name='editar_registro'),
    path('excluir/<int:registro_id>/', excluir_registro, name='excluir_registro'),
    path('download/excel/', download_excel, name='download_excel'),
    path('download/pdf/', download_pdf, name='download_pdf'),
    path('', lambda request: redirect('login')),  # Redireciona para 'login' quando a URL estiver vazia
]
