from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet

from .filters import AcomodacaoFilter
from .models import Acomodacao, ImagemAcomodacao
from .serializers import AcomodacaoSerializer, ImagemAcomodacaoSerializer


class AcomodacaoViewSet(ModelViewSet):
    queryset = Acomodacao.objects.all()
    serializer_class = AcomodacaoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = AcomodacaoFilter
    ordering_fields = ("titulo_acomodacao", "valor_diaria")
    ordering = ("id",)
    search_fields = ("titulo_acomodacao",)


class ImagemAcomodacaoViewSet(ModelViewSet):
    queryset = ImagemAcomodacao.objects.all()
    serializer_class = ImagemAcomodacaoSerializer
