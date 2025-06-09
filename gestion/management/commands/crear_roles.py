from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from gestion.models import Venta, Reserva, PruebaConduccion, Vehiculo

class Command(BaseCommand):
    help = "Crea grupos con permisos para roles: Administrador, Vendedor, Cliente y Mecanico."

    def handle(self, *args, **kwargs):
        try:
            # Crear grupos
            admin_group, _ = Group.objects.get_or_create(name='Administrador')
            vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
            cliente_group, _ = Group.objects.get_or_create(name='Cliente')
            mecanico_group, _ = Group.objects.get_or_create(name='Mecanico')

            # Asignar permisos a Administrador (todos)
            all_permissions = Permission.objects.all()
            admin_group.permissions.set(all_permissions)
            self.stdout.write(self.style.SUCCESS("Permisos asignados a Administrador"))

            # Asignar permisos a Mecánico (solo Vehículos)
            content_vehiculo = ContentType.objects.get_for_model(Vehiculo)
            permisos_mecanico = Permission.objects.filter(
                content_type=content_vehiculo,
                codename__in=['add_vehiculo', 'change_vehiculo', 'delete_vehiculo']
            )
            mecanico_group.permissions.set(permisos_mecanico)
            self.stdout.write(self.style.SUCCESS("Permisos asignados a Mecanico"))

            # Permisos para Vendedor (Ventas)
            content_venta = ContentType.objects.get_for_model(Venta)
            permisos_vendedor = Permission.objects.filter(
                content_type=content_venta,
                codename__in=['add_venta', 'change_venta', 'view_venta']
            )
            vendedor_group.permissions.set(permisos_vendedor)
            self.stdout.write(self.style.SUCCESS("Permisos asignados a Vendedor"))

            # Permisos para Cliente (Reservas y Pruebas)
            content_reserva = ContentType.objects.get_for_model(Reserva)
            content_prueba = ContentType.objects.get_for_model(PruebaConduccion)
            permisos_cliente = Permission.objects.filter(
                content_type__in=[content_reserva, content_prueba],
                codename__in=[
                    'add_reserva', 'change_reserva', 'view_reserva',
                    'add_pruebaconduccion', 'change_pruebaconduccion', 'view_pruebaconduccion'
                ]
            )
            cliente_group.permissions.set(permisos_cliente)
            self.stdout.write(self.style.SUCCESS("Permisos asignados a Cliente"))

            self.stdout.write(self.style.SUCCESS("Grupos y permisos configurados correctamente"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error al configurar roles: {e}"))