
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from gestion.models import Vehiculo, Reserva, PruebaConduccion, Venta
from gestion.forms import PruebaConduccionForm, ReservaForm, VentaForm
from gestion.mixins import RoleRequiredMixin, VehiculoDisponibleMixin


# --- Vistas Vehículo ---
class VehiculoListView(LoginRequiredMixin, ListView):
    model = Vehiculo
    template_name = 'gestion/vehiculo_list.html'
    context_object_name = 'vehiculos'

class VehiculoCreateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, CreateView):
    model = Vehiculo
    template_name = 'gestion/vehiculo_form.html'
    fields = '__all__'
    success_url = reverse_lazy('vehiculo_list')
    permission_required = 'gestion.add_vehiculo'
    required_roles = ['Administrador', 'Mecanico']  # Admin y Mecánico pueden crear

class VehiculoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Vehiculo
    template_name = 'gestion/vehiculo_form.html'
    fields = '__all__'
    success_url = reverse_lazy('vehiculo_list')
    permission_required = 'gestion.change_vehiculo'
    required_roles = ['Administrador', 'Mecanico']  # Admin y Mecánico pueden editar

class VehiculoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Vehiculo
    template_name = 'gestion/vehiculo_confirm_delete.html'
    success_url = reverse_lazy('vehiculo_list')
    permission_required = 'gestion.delete_vehiculo'
    required_roles = ['Administrador', 'Mecanico']  # Admin y Mecánico pueden borrar


# --- Vistas Reserva ---
class ReservaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Reserva
    template_name = 'gestion/reserva_list.html'
    context_object_name = 'reservas'
    permission_required = 'gestion.view_reserva'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            return Reserva.objects.all()
        elif user.groups.filter(name='Cliente').exists():
            return Reserva.objects.filter(cliente=user)
        elif user.groups.filter(name='Vendedor').exists():
            # Vendedor podría ver todas reservas o solo las que gestione, según diseño:
            return Reserva.objects.all()
        else:
            return Reserva.objects.none()

class ReservaCreateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, CreateView):
    model = Reserva
    template_name = 'gestion/reserva_form.html'
    form_class = ReservaForm
    success_url = reverse_lazy('reserva_list')
    permission_required = 'gestion.add_reserva'
    required_roles = ['Cliente']  # Solo clientes pueden reservar

    @transaction.atomic
    def form_valid(self, form):
        form.instance.cliente = self.request.user
        response = super().form_valid(form)
        vehiculo = form.instance.vehiculo
        vehiculo.estado = 'reservado'
        vehiculo.save()
        return response

class ReservaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, UpdateView):
    model = Reserva
    template_name = 'gestion/reserva_form.html'
    form_class = ReservaForm
    success_url = reverse_lazy('reserva_list')
    permission_required = 'gestion.change_reserva'
    required_roles = ['Cliente', 'Administrador', 'Vendedor']  # Quienes puedan editar

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Vendedor').exists():
            return Reserva.objects.all()
        return Reserva.objects.filter(cliente=user)

    @transaction.atomic
    def form_valid(self, form):
        if form.instance.cliente != self.request.user and not self.request.user.has_perm('gestion.change_reserva'):
            return self.handle_no_permission()

        original_reserva = Reserva.objects.get(pk=form.instance.pk)
        response = super().form_valid(form)

        if original_reserva.estado != form.instance.estado and form.instance.estado == 'cancelada':
            vehiculo = form.instance.vehiculo
            vehiculo.estado = 'disponible'
            vehiculo.save()

        return response

class ReservaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DeleteView):
    model = Reserva
    template_name = 'gestion/reserva_confirm_delete.html'
    success_url = reverse_lazy('reserva_list')
    permission_required = 'gestion.delete_reserva'
    required_roles = ['Cliente', 'Administrador', 'Vendedor']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Vendedor').exists():
            return Reserva.objects.all()
        return Reserva.objects.filter(cliente=user)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        reserva = self.get_object()
        vehiculo = reserva.vehiculo
        response = super().delete(request, *args, **kwargs)

        vehiculo.estado = 'disponible'
        vehiculo.save()
        return response


# --- Vistas Prueba de Conducción ---
class PruebaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = PruebaConduccion
    template_name = 'gestion/prueba_list.html'
    context_object_name = 'pruebas'
    permission_required = 'gestion.view_pruebaconduccion'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            return PruebaConduccion.objects.all()
        elif user.groups.filter(name='Cliente').exists():
            return PruebaConduccion.objects.filter(cliente=user)
        elif user.groups.filter(name='Vendedor').exists():
            # Vendedor podría ver todas pruebas o solo las asignadas:
            return PruebaConduccion.objects.all()
        else:
            return PruebaConduccion.objects.none()

class PruebaCreateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, CreateView):
    model = PruebaConduccion
    form_class = PruebaConduccionForm
    template_name = 'gestion/prueba_form.html'
    success_url = reverse_lazy('prueba_list')
    permission_required = 'gestion.add_pruebaconduccion'
    required_roles = ['Cliente']  # Solo cliente puede agendar pruebas

    def form_valid(self, form):
        form.instance.cliente = self.request.user
        return super().form_valid(form)

class PruebaUpdateView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, UpdateView):
    model = PruebaConduccion
    template_name = 'gestion/prueba_form.html'
    fields = ['fecha_hora', 'vendedor']
    success_url = reverse_lazy('prueba_list')
    permission_required = 'gestion.change_pruebaconduccion'
    required_roles = ['Cliente', 'Administrador', 'Vendedor']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Vendedor').exists():
            return PruebaConduccion.objects.all()
        return PruebaConduccion.objects.filter(cliente=user)

    def form_valid(self, form):
        if form.instance.cliente != self.request.user and not self.request.user.has_perm('gestion.change_pruebaconduccion'):
            return self.handle_no_permission()
        return super().form_valid(form)

class PruebaDeleteView(LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, DeleteView):
    model = PruebaConduccion
    template_name = 'gestion/prueba_confirm_delete.html'
    success_url = reverse_lazy('prueba_list')
    permission_required = 'gestion.delete_pruebaconduccion'
    required_roles = ['Cliente', 'Administrador', 'Vendedor']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists() or user.groups.filter(name='Vendedor').exists():
            return PruebaConduccion.objects.all()
        return PruebaConduccion.objects.filter(cliente=user)


# --- Vistas Venta ---
class VentaListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Venta
    template_name = 'gestion/venta_list.html'
    context_object_name = 'ventas'
    permission_required = 'gestion.view_venta'

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.groups.filter(name='Administrador').exists():
            return Venta.objects.all()
        elif user.groups.filter(name='Vendedor').exists():
            return Venta.objects.filter(vendedor=user)
        else:
            return Venta.objects.none()

class VentaCreateView(VehiculoDisponibleMixin, LoginRequiredMixin, PermissionRequiredMixin, RoleRequiredMixin, CreateView):
    model = Venta
    template_name = 'gestion/venta_form.html'
    form_class = VentaForm
    success_url = reverse_lazy('venta_list')
    permission_required = 'gestion.add_venta'
    required_roles = ['Vendedor']  # Solo vendedores pueden crear ventas

    def form_valid(self, form):
        form.instance.vendedor = self.request.user
        response = super().form_valid(form)

        vehiculo = form.instance.vehiculo
        vehiculo.estado = 'vendido'
        vehiculo.save()

        return response


from django.shortcuts import render
from django.db.models import Q, F, Count, Avg, ExpressionWrapper, DurationField
from django.db.models.functions import Now
from django.db.models import Sum
from gestion.models import Vehiculo, Venta, Reserva

def consultas_avanzadas(request):
    # 1. Filtrar vehículos con Q
    vehiculos_filtrados = Vehiculo.objects.filter(
        Q(marca__icontains='Toyota') | Q(modelo__icontains='Corolla'),
        precio__lte=20000,
        tipo='SUV'
    )

    # 2. Usar F para calcular ganancia (precio - coste ficticio, por ejemplo)
    # Suponemos un coste fijo para demo (ejemplo 15000)
    vehiculos_ganancia = vehiculos_filtrados.annotate(
        ganancia=F('precio') - 15000  # Ajusta si tienes campo coste real
    )

    # 3. Total de ventas por vendedor
    ventas_por_vendedor = Venta.objects.values('vendedor__username').annotate(
        total_ventas=Sum('monto')
    ).order_by('-total_ventas')

    # 4. Promedio de días entre reserva y venta
    # Suponemos que tienes campo fecha en Reserva y Venta relacionados por vehiculo
    # Primero unimos las reservas con ventas para ese vehículo
    # Nota: Esto es solo aproximado, depende cómo esté la relación exacta en tu modelo

    # Creamos queryset que junta reservas y ventas (solo vehículos con ambas)
    from django.db.models import OuterRef, Subquery
    from django.db.models.functions import Cast
    from django.db.models import DateTimeField

    # Subquery para obtener fecha de venta del vehículo relacionado a reserva
    venta_fecha_subquery = Venta.objects.filter(
        vehiculo=OuterRef('vehiculo')
    ).values('fecha')[:1]

    reservas_con_venta = Reserva.objects.annotate(
        fecha_venta=Subquery(venta_fecha_subquery, output_field=DateTimeField())
    ).exclude(fecha_venta=None)

    # Ahora calculamos la diferencia de días (fecha_venta - fecha_reserva)
    reservas_con_venta = reservas_con_venta.annotate(
        diferencia=ExpressionWrapper(
            F('fecha_venta') - F('fecha_reserva'),
            output_field=DurationField()
        )
    )

    promedio_dias = reservas_con_venta.aggregate(
        promedio=Avg('diferencia')
    )['promedio']

    # 5. Vehículos más reservados y vendidos

    vehiculos_mas_reservados = Vehiculo.objects.annotate(
        reservas_count=Count('reserva')
    ).order_by('-reservas_count')[:5]

    vehiculos_mas_vendidos = Vehiculo.objects.annotate(
        ventas_count=Count('venta')
    ).order_by('-ventas_count')[:5]

    context = {
        'vehiculos_ganancia': vehiculos_ganancia,
        'ventas_por_vendedor': ventas_por_vendedor,
        'promedio_dias': promedio_dias,
        'vehiculos_mas_reservados': vehiculos_mas_reservados,
        'vehiculos_mas_vendidos': vehiculos_mas_vendidos,
    }
    return render(request, 'gestion/consultas_avanzadas.html', context)