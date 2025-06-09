from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    favoritos = models.ManyToManyField('Vehiculo', blank=True, related_name='favoritos_por')

    def __str__(self):
        return self.user.username


class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('segunda_mano', 'Segunda mano'),
    ]
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('vendido', 'Vendido'),
        ('reservado', 'Reservado'),
        ('mantenimiento', 'Mantenimiento'),
    ]

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    imagen = models.ImageField(upload_to='vehiculos/', blank=True, null=True)
    proximo_servicio = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano})"

    def necesita_mantenimiento(self):
        return self.proximo_servicio and self.proximo_servicio < timezone.now().date()


class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservas')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    fecha_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.cliente.username} para {self.vehiculo}"


class PruebaConduccion(models.Model):
    fecha_hora = models.DateTimeField()
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pruebas')
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pruebas_vendidas')

    def __str__(self):
        return f"Prueba de {self.cliente.username} con vendedor {self.vendedor.username if self.vendedor else 'Sin asignar'} el {self.fecha_hora}"


class Venta(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ventas')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')
    fecha = models.DateTimeField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta de {self.vehiculo} a {self.cliente.username} por {self.monto}"