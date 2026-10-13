from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings


class Reserva(models.Model):
    hospede = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservas"
    )
    acomodacao = models.ForeignKey(
        "acomodacoes.Acomodacao", on_delete=models.CASCADE, related_name="reservas"
    )
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        if self.data_inicio and self.data_fim and self.acomodacao:
            dias = (self.data_fim - self.data_inicio).days
            if dias <= 0:
                raise ValidationError(
                    {"data_fim": "A data final deve ser posterior à data inicial."}
                )
            self.valor_total = dias * self.acomodacao.valor_diaria
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.hospede} - {self.acomodacao} - {self.data_inicio} - {self.data_fim} - {self.valor_total}"
