from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import VehiculoViewSet, VentaViewSet, ReservaViewSet, PruebaViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'vehiculos', VehiculoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'pruebas', PruebaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]