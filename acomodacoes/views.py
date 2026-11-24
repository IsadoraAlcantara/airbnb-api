from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=False, methods=['get'], url_path='meus-anuncios', permission_classes=[IsAuthenticated])
    def meus_anuncios(self, request):
        # Filtra apenas as acomodações onde o proprietário é o usuário logado
        minhas_acomodacoes = Acomodacao.objects.filter(
            proprietario=request.user
        ).order_by('-id')
        
        serializer = self.get_serializer(minhas_acomodacoes, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Usuário logado vê todas as publicadas + os próprios rascunhos
            return Acomodacao.objects.filter(
                Q(status_hospedagem=Acomodacao.Status.PUBLISHED) | Q(proprietario=user)
            )
        # Visitante não logado vê apenas as publicadas
        return Acomodacao.objects.filter(status_hospedagem=Acomodacao.Status.PUBLISHED)

    def perform_create(self, serializer):
        serializer.save(proprietario=self.request.user)

    def perform_update(self, serializer):
        # Impede que um usuário logado edite a acomodação de outro anfitrião
        if serializer.instance.proprietario != self.request.user:
            raise PermissionDenied(
                "Você não tem permissão para editar esta acomodação."
            )
        serializer.save()

    def perform_destroy(self, instance):
        # Impede que um usuário logado apague a acomodação de outro anfitrião
        if instance.proprietario != self.request.user:
            raise PermissionDenied(
                "Você não tem permissão para excluir esta acomodação."
            )
        instance.delete()


class ImagemAcomodacaoViewSet(ModelViewSet):
    queryset = ImagemAcomodacao.objects.all()
    serializer_class = ImagemAcomodacaoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ImagemAcomodacao.objects.filter(
                Q(acomodacao__status_hospedagem=Acomodacao.Status.PUBLISHED)
                | Q(acomodacao__proprietario=user)
            )
        return ImagemAcomodacao.objects.filter(
            acomodacao__status_hospedagem=Acomodacao.Status.PUBLISHED
        )
