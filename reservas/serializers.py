from datetime import date
from decimal import Decimal
from rest_framework import serializers

from .models import Reserva
from acomodacoes.serializers import AcomodacaoSerializer


class ReservaSerializer(serializers.ModelSerializer):
    acomodacao = AcomodacaoSerializer(read_only=True)
    valor_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Reserva
        fields = (
            "id",
            "acomodacao",
            "data_inicio",
            "data_fim",
            "valor_total",
        )

    def validate_data_inicio(self, value):
        hoje = date.today()
        if hoje > value:
            raise serializers.ValidationError(
                "A reserva deve ser criada no mínimo no dia da data início"
            )
        return value

    def validate(self, attrs):
        data_inicio = attrs.get(
            "data_inicio", getattr(self.instance, "data_inicio", None)
        )
        data_fim = attrs.get("data_fim", getattr(self.instance, "data_fim", None))

        if data_inicio and data_fim and data_fim <= data_inicio:
            raise serializers.ValidationError(
                {"data_fim": "A data de fim deve ser posterior à data de início."}
            )

        return attrs

    # def validate_valor_total(self, value):
    #     if value <= Decimal("0"):
    #         raise serializers.ValidationError("O valor total deve ser maior que zero.")
    #     return value
