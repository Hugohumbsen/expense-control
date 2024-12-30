from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum

from myapp.models import Registro
from .forms import LoginForm, RegistroForm

def login_view(request):
    # Verifique se o usuário já está autenticado
    #if request.user.is_authenticated:
       # return redirect('registro')  # Redireciona para 'registro' se já estiver logado

    # Lógica de login
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            senha = form.cleaned_data['senha']

            # Tenta autenticar o usuário
            user = authenticate(request, username=username, password=senha)

            if user is not None:
                login(request, user)
                messages.success(request, "Login realizado com sucesso!")
                return redirect('registro')  # Redireciona para 'registro' após login bem-sucedido
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

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona para a tela de login após deslogar

def relatorio(request):
    mes_selecionado = request.POST.get('mes', '')
    categoria_selecionada = request.POST.get('categoria', '')

    # Filtrando os registros com base nos filtros selecionados
    registros = Registro.objects.all()

    if mes_selecionado:
        registros = registros.filter(mes=mes_selecionado)
    
    if categoria_selecionada:
        registros = registros.filter(categoria=categoria_selecionada)

    # Calcular totais por categoria, caso necessário
    totais_categoria = registros.values('categoria').annotate(total_gasto=Sum('preco'))

    context = {
        'registros': registros,
        'totais_categoria': totais_categoria,
        'mes_selecionado': mes_selecionado,
        'categoria_selecionada': categoria_selecionada,
    }

    return render(request, 'relatorio.html', context)