from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseBadRequest
from gestion.models import Vehiculo
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect

class RoleRequiredMixin(UserPassesTestMixin):
    required_roles = []

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        return user.is_authenticated and any(
            group.name in self.required_roles for group in user.groups.all()
        )

    def handle_no_permission(self):
        raise PermissionDenied("No tienes permisos para acceder a esta vista.")


class VehiculoDisponibleMixin:
    def form_valid(self, form):
        vehiculo = form.cleaned_data.get('vehiculo')
        if vehiculo and vehiculo.estado != 'disponible':
            messages.error(self.request, "Este vehículo no está disponible.")
            return redirect('vehiculo_list')
        return super().form_valid(form)