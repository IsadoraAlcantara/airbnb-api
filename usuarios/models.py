from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    data_inicio_anfitriao = models.DateField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    acomodacao = models.ManyToManyField(
        "acomodacoes.Acomodacao",
        through="reservas.Reserva",
        related_name="acomodacoes_reservadas",
    )

    def __str__(self):
        return f"{self.username} - {self.email} - {self.cpf} - {self.telefone}"