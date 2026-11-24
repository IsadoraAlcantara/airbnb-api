from django.conf import settings
from uploader.models import Image
from django.db import models


class Acomodacao(models.Model):
    class CategoriaAcomodacao(models.TextChoices):
        ESPACO_INTEIRO = "Espaço inteiro"
        QUARTO_PRIVATIVO = "Quarto privativo"
        QUARTO_HOTEL = "Quarto hotel"
        QUARTO_COMPARTILHADO = "Quarto compartilhado"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Rascunho"
        PUBLISHED = "PUBLISHED", "Publicado"

    titulo_acomodacao = models.CharField(max_length=50, blank=True)
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    qtd_quartos = models.PositiveIntegerField(default=0, blank=True, null=True)
    qtd_banheiros = models.PositiveIntegerField(default=0, blank=True, null=True)
    qtd_camas = models.PositiveIntegerField(default=0, blank=True, null=True)
    max_hospedes = models.PositiveIntegerField(default=1, blank=True, null=True)
    categoria_acomodacao = models.CharField(
        max_length=30,
        choices=CategoriaAcomodacao.choices,
        default=CategoriaAcomodacao.ESPACO_INTEIRO,
        blank=True
    )
    tipo_acomodacao = models.CharField(max_length=40, default="Casa", blank=True)
    descricao_acomodacao = models.CharField(max_length=500, blank=True, null=True   )
    status_hospedagem = models.CharField(
        choices=Status.choices, default=Status.DRAFT
    )

    logradouro = models.CharField(max_length=150, blank=True, null=True)
    numero_hospedagem = models.CharField(max_length=20, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=40, blank=True, null=True)
    cep = models.CharField(max_length=9, blank=True, null=True)

    proprietario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="acomodacoes",
    )
    hospedes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="reservas.Reserva",
        related_name="acomodacoes_reservadas",
        blank=True
    )

    def __str__(self):
        return f"{self.titulo_acomodacao} - R$ {self.valor_diaria} - {self.categoria_acomodacao} {self.qtd_quartos} - {self.qtd_banheiros} - {self.qtd_camas} - {self.max_hospedes} - {self.status_hospedagem}"


class ImagemAcomodacao(models.Model):
    acomodacao = models.ForeignKey(
        Acomodacao,
        related_name='imagens',
        on_delete=models.CASCADE,
    )
    imagem = models.ImageField(upload_to="acomodacoes/%Y/%m/", blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.imagem} - {self.acomodacao}"
