from django.urls import path
from . import views

urlpatterns = [
    # --- VISTAS DE CATÁLOGO ---
    # Catálogo principal (Alimentos)
    path('', views.catalogo, name='catalogo'),
    
    # Nuevo catálogo exclusivo para Agua Purificada
    path('agua/', views.catalogo_agua, name='catalogo_agua'),

    # --- GESTIÓN DEL CARRITO ---
    # Ver el resumen de la compra
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    
    # Agregar productos (Soporta 'alimento' o 'bidon' gracias a <str:tipo_producto>)
    path('agregar/<str:tipo_producto>/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    
    # Eliminar y editar usando la item_key única (ej: 'ali_1' o 'bid_1')
    path('eliminar/<str:item_key>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('editar-cantidad/<str:item_key>/', views.editar_cantidad_carrito, name='editar_cantidad_carrito'),
    
    # --- PROCESO DE PAGO ---
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),
]