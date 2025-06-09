from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.VehiculoListView.as_view(), name='vehiculo_list'),  # Página por defecto

    # Vehículo
    path('vehiculos/', views.VehiculoListView.as_view(), name='vehiculo_list'),
    path('vehiculos/crear/', views.VehiculoCreateView.as_view(), name='vehiculo_create'),
    path('vehiculos/<int:pk>/editar/', views.VehiculoUpdateView.as_view(), name='vehiculo_update'),
    path('vehiculos/<int:pk>/eliminar/', views.VehiculoDeleteView.as_view(), name='vehiculo_delete'),

    # Reserva
    path('reservas/', views.ReservaListView.as_view(), name='reserva_list'),
    path('reservas/crear/', views.ReservaCreateView.as_view(), name='reserva_create'),
    path('reservas/<int:pk>/editar/', views.ReservaUpdateView.as_view(), name='reserva_update'),
    path('reservas/<int:pk>/eliminar/', views.ReservaDeleteView.as_view(), name='reserva_delete'),

    # Prueba de Conducción
    path('pruebas/', views.PruebaListView.as_view(), name='prueba_list'),
    path('pruebas/crear/', views.PruebaCreateView.as_view(), name='prueba_create'),
    path('pruebas/<int:pk>/editar/', views.PruebaUpdateView.as_view(), name='prueba_update'),
    path('pruebas/<int:pk>/eliminar/', views.PruebaDeleteView.as_view(), name='prueba_delete'),

    # Venta
    path('ventas/', views.VentaListView.as_view(), name='venta_list'),
    path('ventas/crear/', views.VentaCreateView.as_view(), name='venta_create'),


    path('gestion/consultas/', views.consultas_avanzadas, name='consultas_avanzadas')

]