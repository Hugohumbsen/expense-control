from django.core.validators import MinValueValidator
from django.db import models

class Registro(models.Model):
    CATEGORIAS = [
        ('casa', 'Produtos de Casa'),
        ('mercado', 'Mercado'),
        ('farmacia', 'Farmácia'),
        ('lazer', 'Lazer'),
        ('poupanca', 'Poupança'),
        ('transporte', 'Transporte'),
        ('roupa', 'Roupa'),
    ]

    STATUS_PAGAMENTO = [
        ('pago', 'Pago'),
        ('nao_pago', 'Não Pago'),
    ]

    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Preço")
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, verbose_name="Categoria")
    status_pagamento = models.CharField(max_length=10, choices=STATUS_PAGAMENTO, verbose_name="Status de Pagamento")
    mes = models.IntegerField(verbose_name="Mês", default=1)
    ano = models.IntegerField(
        verbose_name="Ano", 
        default=2025,
        validators=[MinValueValidator(2025)]  # Impede o ano de ser inferior a 2025
    )
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")

    def get_mes_nome(self):
        meses = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        return meses[self.mes - 1]

    def __str__(self):
        return f"{self.descricao} - {self.preco} ({self.mes}/{self.ano})"

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
