from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from myapp.models import Registro
from .forms import LoginForm, RegistroForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            senha = form.cleaned_data['senha']

            user = authenticate(request, username=username, password=senha)

            if user is not None:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('registro')  # Redireciona para a página inicial
            else:
                messages.error(request, "Credenciais inválidas. Tente novamente.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro adicionado com sucesso!")
            return redirect('registro')
        else:
            messages.error(request, "Erro ao adicionar registro. Verifique os dados.")
    else:
        form = RegistroForm()

    registros = Registro.objects.all().order_by('-data_hora')
    return render(request, 'registro.html', {'form': form, 'registros': registros})
