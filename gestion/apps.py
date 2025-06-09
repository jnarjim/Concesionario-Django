from django.apps import AppConfig

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'

    def ready(self):
        try:
            from django.contrib.auth.models import Group, Permission
            from django.contrib.contenttypes.models import ContentType
            from gestion.models import Venta, Reserva, PruebaConduccion, Vehiculo

            # Crear grupos
            roles = ['Administrador', 'Vendedor', 'Mecánico', 'Cliente']
            for role in roles:
                Group.objects.get_or_create(name=role)

            # Permisos para Administrador
            admin_group, _ = Group.objects.get_or_create(name='Administrador')
            all_permissions = Permission.objects.all()
            admin_group.permissions.set(all_permissions)

            # Permisos para Vendedor
            vendedor_group, _ = Group.objects.get_or_create(name='Vendedor')
            content_venta = ContentType.objects.get_for_model(Venta)
            permisos_vendedor = Permission.objects.filter(
                content_type=content_venta,
                codename__in=['add_venta', 'change_venta', 'view_venta']
            )
            vendedor_group.permissions.set(permisos_vendedor)

            # Permisos para Cliente
            cliente_group, _ = Group.objects.get_or_create(name='Cliente')
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
        except Exception:
            # Puede ser django.db.utils.OperationalError o django.db.utils.ProgrammingError
            # Ignora errores que ocurren cuando la DB o las tablas aún no existen
            pass