from django.conf import settings
from uploader.models import Image
from django.db import models

# class Estado(models.Model):
#     nome_estado = models.CharField(max_length=50)

#     def __str__(self):
#         return f"{self.nome_estado}"


# class Cidade(models.Model):
#     cod_estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
#     nome_cidade = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.nome_cidade}"


# class Bairro(models.Model):
#     cod_cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
#     nome_bairro = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.nome_bairro}"


# class Endereco(models.Model):
#     cod_bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
#     nome_logradouro = models.CharField(max_length=150)
#     numero_endereco = models.IntegerField()

#     def __str__(self):
#         return f"{self.nome_logradouro} - {self.numero_endereco}"


class Acomodacao(models.Model):
    class CategoriaAcomodacao(models.TextChoices):
        ESPACO_INTEIRO = "espaço inteiro"
        QUARTO_PRIVATIVO = "quarto privativo"
        QUARTO_HOTEL = "quarto hotel"
        QUARTO_COMPARTILHADO = "quarto compartilhado"

    titulo_acomodacao = models.CharField(max_length=100)
    valor_diaria = models.DecimalField(max_digits=10, decimal_places=2)
    qtd_quartos = models.PositiveIntegerField(default=0)
    qtd_banheiros = models.PositiveIntegerField(default=0)
    qtd_camas = models.PositiveIntegerField(default=0)
    max_hospedes = models.PositiveIntegerField(default=1)
    categoria_acomodacao = models.CharField(
        max_length=30,
        choices=CategoriaAcomodacao.choices,
        default=CategoriaAcomodacao.ESPACO_INTEIRO,
    )
    tipo_acomodacao = models.CharField(max_length=40, default="Casa")
    status_hospedagem = models.BooleanField(default=True)

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
    # endereco = models.ForeignKey(
    #     Endereco, on_delete=models.CASCADE, null=True, blank=True
    # )
    hospedes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="reservas.Reserva",
        related_name="acomodacoes_reservadas",
    )

    def __str__(self):
        return f"{self.titulo_acomodacao} - R$ {self.valor_diaria} - {self.categoria_acomodacao} {self.qtd_quartos} - {self.qtd_banheiros} - {self.qtd_camas} - {self.max_hospedes} - {self.status_hospedagem}"


class ImagemAcomodacao(models.Model):
    acomodacao = models.ForeignKey(
        Acomodacao,
        on_delete=models.CASCADE,
    )
    imagem_acomodacao = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name="+",
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return f"{self.imagem_acomodacao} - {self.acomodacao}"
