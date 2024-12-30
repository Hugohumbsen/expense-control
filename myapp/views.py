from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm, RegistroForm

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            primeiro_nome = form.cleaned_data['primeiro_nome']
            ultimo_nome = form.cleaned_data['ultimo_nome']
            senha = form.cleaned_data['senha']

            # Autentica com base no banco de dados
            try:
                from django.contrib.auth.models import User
                usuario = User.objects.get(first_name=primeiro_nome, last_name=ultimo_nome)
                user = authenticate(request, username=usuario.username, password=senha)

                if user is not None:
                    login(request, user)
                    messages.success(request, "Login realizado com sucesso!")
                    return redirect('home')  # Redireciona para a página inicial
                else:
                    messages.error(request, "Senha incorreta. Tente novamente.")
            except User.DoesNotExist:
                messages.error(request, "Usuário não encontrado.")
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
