from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from .filters import AcomodacaoFilter
from .models import Acomodacao, ImagemAcomodacao
from .serializers import AcomodacaoSerializer, ImagemAcomodacaoSerializer


class AcomodacaoViewSet(ModelViewSet):
    queryset = Acomodacao.objects.all()
    serializer_class = AcomodacaoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = AcomodacaoFilter
    ordering_fields = ("titulo_acomodacao", "valor_diaria")
    ordering = ("id",)
    search_fields = (
        "titulo_acomodacao",
        "descricao_acomodacao",
        "cidade",
        "bairro",
        "tipo_acomodacao",
    )


class ImagemAcomodacaoViewSet(ModelViewSet):
    queryset = ImagemAcomodacao.objects.all()
    serializer_class = ImagemAcomodacaoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        # Garante que o usuário só veja e delete fotos das próprias acomodações
        return ImagemAcomodacao.objects.filter(acomodacao__proprietario=self.request.user)

    def perform_create(self, serializer):
        # Valida se a acomodação enviada no FormData pertence ao usuário logado
        acomodacao = serializer.validated_data['acomodacao']
        if acomodacao.proprietario != self.request.user:
            raise PermissionDenied("Você não tem permissão para adicionar fotos nesta acomodação.")
        serializer.save()
