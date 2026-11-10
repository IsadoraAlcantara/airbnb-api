from rest_framework.viewsets import ModelViewSet

from .models import Reserva
from .serializers import ReservaSerializer


class ReservaViewSet(ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer