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
            "data_inicio",
            "data_fim",
            "valor_total",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["acomodacao"] = AcomodacaoSerializer(instance.acomodacao).data
        return representation

    def validate(self, attrs):
        # 1. Recupera as datas tratadas pelo DRF
        data_inicio = attrs.get("data_inicio") or (
            self.instance.data_inicio if self.instance else None
        )
        data_fim = attrs.get("data_fim") or (
            self.instance.data_fim if self.instance else None
        )
        acomodacao = attrs.get("acomodacao") or (
            self.instance.acomodacao if self.instance else None
        )

        # REMOVER
        if not data_inicio or not data_fim or not acomodacao:
            raise serializers.ValidationError(
                {
                    "non_field_errors": [
                        "Os campos data_inicio, data_fim e acomodacao são obrigatórios."
                    ]
                }
            )

        # 2. Pega a data local considerando o TIME_ZONE do settings.py
        hoje = timezone.localdate()
        max_dias_antecedencia = hoje + timedelta(days=MAX_DIAS_ANTECEDENCIA)

        # -------------------------------------------------------------
        # VALIDAÇÃO 1: Data de início no passado
        # -------------------------------------------------------------
        if data_inicio < hoje:
            raise serializers.ValidationError(
                {
                    "data_inicio": f"A data de início ({data_inicio}) não pode ser no passado. Hoje é {hoje}."
                }
            )

        # REMOVER ##################
        # -------------------------------------------------------------
        # VALIDAÇÃO 2: Sequência das datas
        # -------------------------------------------------------------
        # if data_fim <= data_inicio:
        #     raise serializers.ValidationError(
        #         {"data_fim": "A data de fim deve ser posterior à data de início."}
        #     )
        # else: 
        #     dias = (data_fim - data_inicio).days
        #     attrs['valor_total'] = dias * acomodacao.valor_diaria

        # -------------------------------------------------------------
        # VALIDAÇÃO 3: Antecedência máxima
        # -------------------------------------------------------------
        if data_inicio > max_dias_antecedencia:
            raise serializers.ValidationError(
                {
                    "data_inicio": f"Não é possível realizar reservas com mais de {MAX_DIAS_ANTECEDENCIA} dias de antecedência."
                }
            )

        # -------------------------------------------------------------
        # VALIDAÇÃO 4: Sobreposição no Banco
        # -------------------------------------------------------------
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
