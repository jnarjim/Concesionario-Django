
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.utils.timezone import now
from django.shortcuts import redirect
from gestion.models import Vehiculo

class MantenimientoMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.path.startswith('/gestion/') and not request.session.get('mantenimiento_alertado'):
            vehiculos_vencidos = Vehiculo.objects.filter(proximo_servicio__lt=now().date())
            if vehiculos_vencidos.exists():
                messages.warning(request, f"Hay {vehiculos_vencidos.count()} vehículo(s) con mantenimiento vencido.")
                request.session['mantenimiento_alertado'] = True


class RestriccionClienteMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and request.user.groups.filter(name='Cliente').exists():
            if request.path.startswith('/ventas/') or request.path.startswith('/admin-vehiculos/'):
                messages.error(request, "No tienes permiso para acceder a esta sección.")
                return redirect('/gestion/')