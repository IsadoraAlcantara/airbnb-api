from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers

from .models import Reserva
from acomodacoes.serializers import AcomodacaoSerializer
from acomodacoes.models import Acomodacao

MAX_DIAS_ANTECEDENCIA = 365


class ReservaSerializer(serializers.ModelSerializer):
    acomodacao = serializers.PrimaryKeyRelatedField(queryset=Acomodacao.objects.all())
    valor_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Reserva
        fields = (
            "id",
            "acomodacao",
            "hospede",
            "data_inicio",
            "data_fim",
            "valor_total",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["acomodacao"] = AcomodacaoSerializer(instance.acomodacao).data
        return representation

    def validate(self, attrs):
        data_inicio = attrs.get("data_inicio") or (
            self.instance.data_inicio if self.instance else None
        )
        data_fim = attrs.get("data_fim") or (
            self.instance.data_fim if self.instance else None
        )
        acomodacao = attrs.get("acomodacao") or (
            self.instance.acomodacao if self.instance else None
        )

        if not data_inicio or not data_fim or not acomodacao:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Os campos data_inicio, data_fim e acomodacao são obrigatórios."
                    ]
                }
            )

        hoje = timezone.localdate()
        max_dias_antecedencia = hoje + timedelta(days=MAX_DIAS_ANTECEDENCIA)

        if data_inicio < hoje:
            raise serializers.ValidationError(
                {
                    "data_inicio": f"A data de início ({data_inicio}) não pode ser no passado. Hoje é {hoje}."
                }
            )

        if data_inicio > max_dias_antecedencia:
            raise serializers.ValidationError(
                {
                    "data_inicio": f"Não é possível realizar reservas com mais de {MAX_DIAS_ANTECEDENCIA} dias de antecedência."
                }
            )

        sobreposicao_reserva = Reserva.objects.filter(
            acomodacao=acomodacao,
            data_inicio__lt=data_fim,
            data_fim__gt=data_inicio,
        )

        if self.instance:
            sobreposicao_reserva = sobreposicao_reserva.exclude(id=self.instance.id)

        if sobreposicao_reserva.exists():
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "A acomodação já possui reserva confirmada para o período selecionado."
                    ]
                }
            )

        return attrs
