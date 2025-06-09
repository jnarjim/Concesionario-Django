
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Q
from gestion.models import Vehiculo, Venta, Reserva
from gestion.forms import VentaForm

# Tests de lógica de negocio
class LogicaNegocioTest(TestCase):
    def setUp(self):
        self.vendedor = User.objects.create_user(username='vendedor', password='pass')
        self.comprador = User.objects.create_user(username='comprador', password='pass')
        self.vehiculo = Vehiculo.objects.create(
            marca='Toyota', modelo='Corolla', precio=18000, tipo='Sedán'
        )

    def test_crear_venta(self):
        venta = Venta.objects.create(
            vehiculo=self.vehiculo,
            vendedor=self.vendedor,
            cliente=self.comprador,
            monto=self.vehiculo.precio
        )
        self.assertEqual(venta.monto, 18000)

    def test_crear_reserva(self):
        reserva = Reserva.objects.create(
            vehiculo=self.vehiculo,
            cliente=self.comprador,
            fecha_reserva=timezone.now()  # Aquí asegúrate que es el campo correcto en tu modelo
        )
        self.assertEqual(reserva.vehiculo, self.vehiculo)


# Tests para roles y permisos
class PermisosTest(TestCase):
    def setUp(self):
        self.vendedor = User.objects.create_user(username='vendedor', password='pass')
        group = Group.objects.create(name='Vendedor')
        self.vendedor.groups.add(group)
        self.client = Client()
        logged_in = self.client.login(username='vendedor', password='pass')
        self.assertTrue(logged_in)

    def test_vendedor_puede_ver_vehiculos(self):
        response = self.client.get('/gestion/vehiculos/')
        self.assertEqual(response.status_code, 200)

    def test_cliente_no_puede_acceder_ventas(self):
        cliente = User.objects.create_user(username='cliente', password='pass')
        group_cliente = Group.objects.create(name='Cliente')
        cliente.groups.add(group_cliente)
        self.client.logout()
        self.client.login(username='cliente', password='pass')
        response = self.client.get('/gestion/ventas/')
        self.assertNotEqual(response.status_code, 200)  # Debería estar restringido


# Tests para validaciones en formularios
class FormularioVentaTest(TestCase):
    def test_monto_negativo_no_valido(self):
        form_data = {
            'vehiculo': 1,  # Si hay validación ForeignKey, podrías crear un vehiculo para el test
            'vendedor': 1,
            'cliente': 1,
            'monto': -5000,
        }
        form = VentaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('monto', form.errors)


# Tests para consultas avanzadas
class ConsultasTest(TestCase):
    def setUp(self):
        Vehiculo.objects.create(marca='Toyota', modelo='Corolla', precio=15000, tipo='SUV')
        Vehiculo.objects.create(marca='Honda', modelo='Civic', precio=18000, tipo='Sedán')

    def test_busqueda_q(self):
        resultado = Vehiculo.objects.filter(Q(marca__icontains='Toyota') | Q(modelo__icontains='Civic'))
        self.assertEqual(resultado.count(), 2)