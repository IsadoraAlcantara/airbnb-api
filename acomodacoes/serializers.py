from rest_framework import serializers
from decimal import Decimal

from .models import Acomodacao, ImagemAcomodacao
from usuarios.serializers import ProprietarioResumidoSerializer


class ImagemAcomodacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagemAcomodacao
        fields = ("id", "imagem", "acomodacao")


class AcomodacaoSerializer(serializers.ModelSerializer):
    proprietario = ProprietarioResumidoSerializer(read_only=True)
    imagens = ImagemAcomodacaoSerializer(many=True, read_only=True)

    class Meta:
        model = Acomodacao
        fields = (
            "id",
            "proprietario",
            "titulo_acomodacao",
            "descricao_acomodacao",
            "categoria_acomodacao",
            "tipo_acomodacao",
            "valor_diaria",
            "qtd_quartos",
            "qtd_banheiros",
            "qtd_camas",
            "max_hospedes",
            "status_hospedagem",
            "logradouro",
            "numero_hospedagem",
            "bairro",
            "cidade",
            "estado",
            "cep",
            "imagens"
        )

    def get_proprietario(self, obj):
        from usuarios.serializers import UsuarioSerializer

        if obj.proprietario:
            return UsuarioSerializer(obj.proprietario, context=self.context).data
        return None

    def validate_titulo_acomodacao(self, value):
        if not value:
            return ""
        
        titulo_limpo = value.strip()
        if titulo_limpo and len(titulo_limpo) < 3:
            raise serializers.ValidationError(
                "O título da acomodação deve possuir mais do que 3 caracteres"
            )
        return titulo_limpo

    def validate_valor_diaria(self, value):
        if value is not None and value <= Decimal("0"):
            raise serializers.ValidationError(
                "O valor da diária deve ser maior do que zero"
            )
        return value

    def validate_cep(self, value):
        cep_limpo = "".join(filter(str.isdigit, str(value or "")))
        if len(cep_limpo) != 8:
            raise serializers.ValidationError("Informe um CEP válido com 8 dígitos.")
        return value