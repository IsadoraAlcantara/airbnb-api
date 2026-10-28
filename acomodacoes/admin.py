from django.contrib import admin

from .models import Acomodacao, Bairro, Cidade, Endereco, Estado


@admin.register(Acomodacao)
class AcomodacaoAdmin(admin.ModelAdmin):
    list_display = (
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
    search_fields = ("titulo_acomodacao",)


@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome_bairro",
    )
    search_fields = ("nome_bairro",)


@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome_cidade",
    )
    search_fields = ("nome_cidade",)


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome_logradouro",
        "numero_endereco",
    )
    search_fields = (
        "nome_logradouro",
        "numero_endereco",
    )


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome_estado",
    )
    search_fields = ("nome_estado",)
