from django import forms
from django.core.exceptions import ValidationError
from gestion.models import Reserva, PruebaConduccion, Venta


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['vehiculo', 'estado']

    def clean_vehiculo(self):
        vehiculo = self.cleaned_data.get('vehiculo')
        if vehiculo and vehiculo.estado != 'disponible':
            raise ValidationError("El vehículo no está disponible para reservas.")
        return vehiculo


class PruebaConduccionForm(forms.ModelForm):
    class Meta:
        model = PruebaConduccion
        fields = ['fecha_hora', 'vendedor']
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_fecha_hora(self):
        fecha = self.cleaned_data['fecha_hora']
        if PruebaConduccion.objects.filter(fecha_hora=fecha).exists():
            raise ValidationError("Ya hay una prueba en ese horario.")
        return fecha


class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['vehiculo', 'cliente', 'monto']

    def clean_vehiculo(self):
        vehiculo = self.cleaned_data['vehiculo']
        if vehiculo.estado != 'disponible':
            raise ValidationError("Este vehículo ya fue vendido o no está disponible.")
        return vehiculo