from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('editar-cantidad/<int:producto_id>/', views.editar_cantidad_carrito, name='editar_cantidad_carrito'),
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
]
