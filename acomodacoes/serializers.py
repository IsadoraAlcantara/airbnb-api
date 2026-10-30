from rest_framework import serializers
from decimal import Decimal

from .models import Acomodacao, ImagemAcomodacao


class AcomodacaoSerializer(serializers.ModelSerializer):
    proprietario = serializers.SerializerMethodField()

    class Meta:
        model = Acomodacao
        fields = (
            "id",
            "proprietario",
            "titulo_acomodacao",
            "valor_diaria",
            "qtd_quartos",
            "qtd_banheiros",
            "qtd_camas",
            "max_hospedes",
            "status_hospedagem",
        )

    def get_proprietario(self, obj):
        from usuarios.serializers import UsuarioSerializer

        if obj.proprietario:
            return UsuarioSerializer(obj.proprietario, context=self.context).data
        return None

    def validate_titulo_acomodacao(self, value):
        titulo_limpo = value.strip()
        if len(titulo_limpo) < 3:
            raise serializers.ValidationError(
                "O título da acomodação deve possuir mais do que 3 caracteres"
            )
        return titulo_limpo

    def validate_valor_diaria(self, value):
        if value <= Decimal("0"):
            raise serializers.ValidationError(
                "O valor da diária deve ser maior do que zero"
            )
        return value


class ImagemAcomodacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagemAcomodacao
        fields = ("id", "imagem_acomodacao")


# class EstadoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Estado
#         fields = (
#             "id",
#             "nome_estado"
#         )

# class CidadeSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Estado
#         fields = (
#             "id",
#             "nome_cidade"
#         )

# class BairroSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Bairro
#         fields = (
#             "id",
#             "nome_bairro"
#         )

# class EnderecoSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Endereco
#         fields = (
#             "id",
#             "nome_logradouro",
#             "numero_endereco"
#         )
