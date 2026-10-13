from datetime import date
import re
from rest_framework import serializers

from .models import Usuario
from reservas.serializers import ReservaSerializer


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    reservas = ReservaSerializer(many=True, read_only=True)

    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "password",
            "cpf",
            "data_nascimento",
            "telefone",
            "first_name",
            "last_name",
            "data_inicio_anfitriao",
            "reservas",
        ]

    def criacao_usuario(self, validated_data):
        return Usuario.objects.create_user(**validated_data)

    def validate_cpf(self, value):
        cpf = re.sub(r"\D", "", value)

        if len(cpf) != 11:
            raise serializers.ValidationError("O CPF deve conter exatamente 11 dígitos")

        if cpf == cpf[0] * 11:
            raise serializers.ValidationError("CPF inválido")

        for i in range(9, 11):
            soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(0, i))
            digito = (soma * 10) % 11
            if digito == 10:
                digito = 0
            if int(cpf[i]) != digito:
                raise serializers.ValidationError("CPF inválido")

        return cpf

    def validate_telefone(self, value):
        telefone = re.sub(r"\D", "", value)

        if len(telefone) not in [10, 11]:
            raise serializers.ValidationError(
                "O telefone deve ter 10 dígitos (fixo com DDD) ou 11 dígitos (celular com DDD)"
            )

        ddd = int(telefone[:2])
        if ddd < 11 or ddd > 99:
            raise serializers.ValidationError("DDD inválido")

        if len(telefone) == 11 and telefone[2] != "9":
            raise serializers.ValidationError(
                "Número de celular deve começar com o dígito 9."
            )

        return telefone

    def validate_data_nascimento(self, value):
        hoje = date.today()
        if value >= hoje:
            raise serializers.ValidationError("A data de nascimento deve ser pelo menos no dia anterior a hoje")

        idade = hoje.year - value.year - ((hoje.month, hoje.day) < (value.month, value.day))

        if idade < 18:
            raise serializers.ValidationError("O usuário deve ter pelo menos 18 anos.")
        return value
