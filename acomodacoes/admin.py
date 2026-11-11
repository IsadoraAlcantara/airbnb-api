from django.contrib import admin

from .models import Acomodacao, ImagemAcomodacao


@admin.register(Acomodacao)
class AcomodacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "proprietario",
        "titulo_acomodacao",
        "categoria_acomodacao",
        "tipo_acomodacao",
        "valor_diaria",
        "qtd_quartos",
        "qtd_banheiros",
        "qtd_camas",
        "max_hospedes",
        "status_hospedagem",
    )
    list_filter = ("estado", "cidade", "status_hospedagem")
    search_fields = (
        "titulo_acomodacao",
        "categoria_acomodacao",
        "cidade",
        "logradouro",
    )


@admin.register(ImagemAcomodacao)
class ImagemAcomodacaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "imagem_acomodacao",
    )
