from django import forms
from .models import Registro
from django.contrib.auth.models import User


class RegistroForm(forms.ModelForm):
    class Meta:
        model = Registro
        fields = ['descricao', 'preco', 'categoria', 'status_pagamento', 'mes', 'ano']
        widgets = {
            'descricao': forms.TextInput(attrs={'placeholder': 'Digite a descrição'}),
            'preco': forms.NumberInput(attrs={'placeholder': 'Digite o preço'}),
            'categoria': forms.Select(),
            'status_pagamento': forms.Select(),
            'mes': forms.NumberInput(attrs={'placeholder': 'Digite o mês (1-12)', 'min': 1, 'max': 12}),
            'ano': forms.NumberInput(attrs={'placeholder': 'Digite o ano'}),
        }


class LoginForm(forms.Form):
    primeiro_nome = forms.CharField(
        max_length=30, 
        label="Primeiro Nome", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu primeiro nome'})
    )
    ultimo_nome = forms.CharField(
        max_length=30, 
        label="Último Nome", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu último nome'})
    )
    senha = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )

    class RegisterUser(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput)
        confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return cleaned_data