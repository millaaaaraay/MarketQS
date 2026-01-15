from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Alimento

# =========================
# CATÁLOGO / INDEX
# =========================
def catalogo(request):
    query = request.GET.get('q')

    if query:
        productos = Alimento.objects.filter(
            Q(nombre__icontains=query) |
            Q(marca__icontains=query)
        )
    else:
        productos = Alimento.objects.all()

    # Contador de productos en el carrito para mostrar en la navbar
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    
    return render(request, 'index.html', {
        'productos': productos,
        'query': query,
        'total_items': total_items
    })


# =========================
# AGREGAR AL CARRITO
# =========================
def agregar_al_carrito(request, producto_id):
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad', 1))
        producto = get_object_or_404(Alimento, id=producto_id)
        
        # Obtenemos el carrito de la sesión
        carrito = request.session.get('carrito', {})

        # Si ya existe, sumamos cantidad
        if str(producto_id) in carrito:
            carrito[str(producto_id)]['cantidad'] += cantidad
        else:
            carrito[str(producto_id)] = {
                'nombre': producto.nombre,
                'precio': int(producto.precio),
                'cantidad': cantidad,
                'imagen': producto.imagen_url
            }

        # Guardamos el carrito actualizado
        request.session['carrito'] = carrito

        # Si es una petición AJAX, devolvemos JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            total_items = sum(item['cantidad'] for item in carrito.values())
            return JsonResponse({'success': True, 'total_items': total_items})

        # Si no es AJAX, redirigimos
        return redirect('catalogo')


# =========================
# VER CARRITO
# =========================
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    # También calculamos total_items por si lo necesitas en el navbar del carrito
    total_items = sum(item['cantidad'] for item in carrito.values())
    
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
        'total_items': total_items
    })


# =========================
# ELIMINAR PRODUCTO DEL CARRITO
# =========================
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    if str(producto_id) in carrito:
        del carrito[str(producto_id)]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('ver_carrito')


# =========================
# EDITAR CANTIDAD DE PRODUCTO EN EL CARRITO
# =========================
def editar_cantidad_carrito(request, producto_id):
    if request.method == "POST":
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        if str(producto_id) in carrito:
            if nueva_cantidad > 0:
                carrito[str(producto_id)]['cantidad'] = nueva_cantidad
            else:
                del carrito[str(producto_id)]
            request.session['carrito'] = carrito
            request.session.modified = True
    return redirect('ver_carrito')


# =========================
# PROCESAR PAGO (NUEVA)
# =========================
def procesar_pago(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    # Por ahora renderizamos una pantalla de carga/espera.
    # Aquí es donde integrarás Webpay, Mercado Pago o Transbank.
    return render(request, 'procesando_pago.html', {
        'total': total,
        'carrito': carrito
    })