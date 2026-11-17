from django_filters import rest_framework as filters

from .models import Acomodacao


class AcomodacaoFilter(filters.FilterSet):
    valor_diaria_minimo = filters.NumberFilter(
        field_name="valor_diaria", lookup_expr="gte"
    )
    valor_diaria_maximo = filters.NumberFilter(
        field_name="valor_diaria", lookup_expr="lte"
    )
    qtd_max_hospedes = filters.NumberFilter(
        field_name="max_hospedes", lookup_expr="gte"
    )
    qtd_quartos_minimo = filters.NumberFilter(
        field_name="qtd_quartos", lookup_expr="gte"
    )
    qtd_banheiros_minimo = filters.NumberFilter(
        field_name="qtd_banheiros", lookup_expr="gte"
    )
    qtd_camas_minimo = filters.NumberFilter(field_name="qtd_camas", lookup_expr="gte")

    class Meta:
        model = Acomodacao
        fields = (
            "valor_diaria_minimo",
            "valor_diaria_maximo",
            "qtd_quartos_minimo",
            "qtd_banheiros_minimo",
            "qtd_camas_minimo",
            "qtd_max_hospedes",
        )
