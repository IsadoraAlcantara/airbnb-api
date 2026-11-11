from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from uploader.router import router as uploader_router
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from acomodacoes.views import AcomodacaoViewSet
from usuarios.views import (
    CustomTokenObtainPairView,
    RegistroUsuarioView,
    PerfilUsuarioView,
)
from reservas.views import ReservaViewSet

router = DefaultRouter()
router.register("acomodacoes", AcomodacaoViewSet, basename="acomodacao")
router.register("reservas", ReservaViewSet, basename="reserva")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/media/", include(uploader_router.urls)),
    
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('api/usuarios/cadastrar/', RegistroUsuarioView.as_view(), name='cadastrar_usuario'),
    path('api/usuarios/me/', PerfilUsuarioView.as_view(), name='perfil_usuario'),
]

urlpatterns += static(settings.MEDIA_ENDPOINT, document_root=settings.MEDIA_ROOT)
