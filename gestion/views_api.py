from rest_framework import viewsets
from .models import Vehiculo, Venta, Reserva, PruebaConduccion
from .serializers import VehiculoSerializer, VentaSerializer, ReservaSerializer, PruebaConduccionSerializer
from rest_framework import permissions

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            if self.request.user.groups.filter(name__in=['Administrador', 'Mecanico']).exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        return [permissions.IsAuthenticated()]

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Admin y Vendedor pueden ver ventas
            if self.request.user.groups.filter(name__in=['Administrador', 'Vendedor']).exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action == 'create':
            # Solo Vendedor puede crear ventas
            if self.request.user.groups.filter(name='Vendedor').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Solo Admin puede modificar o borrar ventas
            if self.request.user.groups.filter(name='Administrador').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        return [permissions.IsAuthenticated()]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Admin, Vendedor y Cliente pueden ver reservas (quizá los clientes sólo las suyas)
            if self.request.user.groups.filter(name__in=['Administrador', 'Vendedor', 'Cliente']).exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action == 'create':
            # Solo Cliente puede crear reservas
            if self.request.user.groups.filter(name='Cliente').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Admin puede modificar o eliminar reservas
            if self.request.user.groups.filter(name='Administrador').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        return [permissions.IsAuthenticated()]

class PruebaViewSet(viewsets.ModelViewSet):
    queryset = PruebaConduccion.objects.all()
    serializer_class = PruebaConduccionSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Admin, Vendedor y Cliente pueden ver pruebas
            if self.request.user.groups.filter(name__in=['Administrador', 'Vendedor', 'Cliente']).exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action == 'create':
            # Solo Cliente puede solicitar pruebas
            if self.request.user.groups.filter(name='Cliente').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Solo Admin puede modificar o eliminar pruebas
            if self.request.user.groups.filter(name='Administrador').exists():
                return [permissions.IsAuthenticated()]
            return [permissions.DenyAll()]
        return [permissions.IsAuthenticated()]