from tkinter import Canvas
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
import openpyxl
from django.contrib.messages import get_messages
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


# View para exibir os registros e adicionar um novo
@login_required
def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro adicionado com sucesso!")
            return redirect('registro')
    else:
        form = RegistroForm()

    registros = Registro.objects.all()
    return render(request, 'registro.html', {'form': form, 'registros': registros})

# View para editar um registro
def editar_registro(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id)
    if request.method == "POST":
        form = RegistroForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro atualizado com sucesso!")
            return redirect('registro')
    else:
        form = RegistroForm(instance=registro)

    return render(request, 'editar_registro.html', {'form': form})

# View para excluir um registro
def excluir_registro(request, registro_id):
    registro = get_object_or_404(Registro, id=registro_id)
    if request.method == "POST":
        registro.delete()
        messages.success(request, "Registro excluído com sucesso!")
        return redirect('registro')

    return render(request, 'confirmar_exclusao.html', {'registro': registro})

def logout_view(request):
    logout(request)
    # Limpa todas as mensagens da sessão
    storage = get_messages(request)
    for _ in storage:
        pass
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

def download_excel(request):
    registros = Registro.objects.all()
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title="Registro"

    sheet.append(["Descrição", "Preço", "Categoria", "Status de Pagamento", "Mês", "Ano", "Data e Hora"])
    # Preencher os dados
    for registro in registro:
        sheet.append([
            registro.descricao,
            registro.preco,
            registro.get_categoria_display(),
            registro.get_status_pagamento_display(),
            registro.get_mes_nome(),
            registro.ano,
            registro.data_hora,
        ])

    # Preparar a resposta para download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=relatorio_gastos.xlsx'
    wb.save(response)
    return response

def download_pdf(request):
    registros = Registro.objects.all()  # Ajuste conforme necessário

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=relatorio_gastos.pdf'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 40, "Relatório de Gastos")

    p.setFont("Helvetica", 10)
    y_position = height - 80
    p.drawString(30, y_position, "Descrição")
    p.drawString(200, y_position, "Preço")
    p.drawString(300, y_position, "Categoria")
    p.drawString(400, y_position, "Status de Pagamento")
    p.drawString(500, y_position, "Mês")
    p.drawString(600, y_position, "Ano")
    p.drawString(700, y_position, "Data e Hora")

    y_position -= 20
    for registro in registros:
        if y_position < 50:  # Adiciona nova página se necessário
            p.showPage()
            p.setFont("Helvetica", 10)
            y_position = height - 40

        p.drawString(30, y_position, registro.descricao)
        p.drawString(200, y_position, str(registro.preco))
        p.drawString(300, y_position, registro.get_categoria_display())
        p.drawString(400, y_position, registro.get_status_pagamento_display())
        p.drawString(500, y_position, registro.get_mes_nome())
        p.drawString(600, y_position, str(registro.ano))
        p.drawString(700, y_position, str(registro.data_hora))
        y_position -= 20

    p.showPage()
    p.save()

    return response


class CustomLoginView(LoginView):
    template_name = 'login.html'  

    def dispatch(self, request, *args, **kwargs):
        
        return super().dispatch(request, *args, **kwargs)