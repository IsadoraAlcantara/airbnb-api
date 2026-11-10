from rest_framework.viewsets import ModelViewSet

from .models import Reserva
from .serializers import ReservaSerializer


class ReservaViewSet(ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def create(self, request, *args, **kwargs):
        print(">>> 2. A VIEWSET RECEBEU O POST NO ENDPOINT CORRETO! <<<")
        return super().create(request, *args, **kwargs)