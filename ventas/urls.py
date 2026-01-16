# ventas/urls.py
from django.urls import path, include  # <--- Agregamos 'include' aquí
from . import views

urlpatterns = [
    # --- VISTAS DE CATÁLOGO ---
    path('', views.catalogo, name='catalogo'),
    path('agua/', views.catalogo_agua, name='catalogo_agua'),

    # --- GESTIÓN DEL CARRITO ---
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('agregar/<str:tipo_producto>/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar/<str:item_key>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('editar-cantidad/<str:item_key>/', views.editar_cantidad_carrito, name='editar_cantidad_carrito'),
    
    # --- PROCESO DE PAGO ---
    path('procesar-pago/', views.procesar_pago, name='procesar_pago'),

    # --- AUTENTICACIÓN ---
    path('registro/', views.registro, name='registro'),
    path('accounts/', include('django.contrib.auth.urls')), # Ahora esto funcionará sin errores
]