from rest_framework import serializers
from .models import Vehiculo, Venta, Reserva, PruebaConduccion
from django.contrib.auth.models import User

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class PruebaConduccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PruebaConduccion
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']