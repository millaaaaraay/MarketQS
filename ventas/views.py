from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from .models import Alimento, Bidon  # Importamos ambos modelos

# =========================
# CATÁLOGO / INDEX
# =========================
def catalogo(request):
    query = request.GET.get('q')
    current_category = request.GET.get('categoria')  # <-- Aquí capturas la categoría

    if query:
        alimentos = Alimento.objects.filter(
            Q(nombre__icontains=query) | Q(marca__icontains=query)
        )
        bidones = Bidon.objects.filter(
            Q(nombre__icontains=query)
        )
    else:
        alimentos = Alimento.objects.all()
        bidones = Bidon.objects.all()

    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())

    return render(request, 'index.html', {
        'alimentos': alimentos,
        'bidones': bidones,
        'query': query,
        'total_items': total_items,
        'current_category': current_category  # <-- enviamos al template
    })



# =========================
# AGREGAR AL CARRITO
# =========================
# Recibe 'tipo_producto' para saber si buscar en Alimento o Bidon
def agregar_al_carrito(request, producto_id, tipo_producto):
    if request.method == "POST":
        cantidad = int(request.POST.get('cantidad', 1))
        
        # Lógica para identificar qué estamos vendiendo
        if tipo_producto == 'alimento':
            producto = get_object_or_404(Alimento, id=producto_id)
            item_key = f"ali_{producto_id}"  # Clave única para la sesión
            nombre_display = f"{producto.marca} - {producto.nombre}"
        else:
            producto = get_object_or_404(Bidon, id=producto_id)
            item_key = f"bid_{producto_id}"  # Clave única para la sesión
            nombre_display = producto.nombre

        # Obtenemos el carrito de la sesión
        carrito = request.session.get('carrito', {})

        # Si ya existe en el carrito, sumamos cantidad
        if item_key in carrito:
            carrito[item_key]['cantidad'] += cantidad
        else:
            carrito[item_key] = {
                'id_real': producto_id,
                'tipo': tipo_producto,
                'nombre': nombre_display,
                'precio': int(producto.precio),
                'cantidad': cantidad,
                'imagen': producto.imagen_url
            }

        # Guardamos el carrito actualizado y marcamos sesión como modificada
        request.session['carrito'] = carrito
        request.session.modified = True

        # Soporte para AJAX (tu script de SweetAlert2)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            total_items = sum(item['cantidad'] for item in carrito.values())
            return JsonResponse({'success': True, 'total_items': total_items})

        return redirect('catalogo')


# =========================
# VER CARRITO
# =========================
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    total_items = sum(item['cantidad'] for item in carrito.values())
    
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'total': total,
        'total_items': total_items
    })


# =========================
# ELIMINAR PRODUCTO DEL CARRITO
# =========================
def eliminar_del_carrito(request, item_key):
    carrito = request.session.get('carrito', {})
    if item_key in carrito:
        del carrito[item_key]
        request.session['carrito'] = carrito
        request.session.modified = True
    return redirect('ver_carrito')


# =========================
# EDITAR CANTIDAD
# =========================
def editar_cantidad_carrito(request, item_key):
    if request.method == "POST":
        nueva_cantidad = int(request.POST.get('cantidad', 1))
        carrito = request.session.get('carrito', {})
        
        if item_key in carrito:
            if nueva_cantidad > 0:
                carrito[item_key]['cantidad'] = nueva_cantidad
            else:
                del carrito[item_key]
            request.session['carrito'] = carrito
            request.session.modified = True
    return redirect('ver_carrito')


# =========================
# PROCESAR PAGO
# =========================
def procesar_pago(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    return render(request, 'procesando_pago.html', {
        'total': total,
        'carrito': carrito
    })


# =========================
# CATALOGO AGUA / BIDONES
# =========================
def catalogo_agua(request):
    bidones = Bidon.objects.all()
    # Para el contador del carrito
    carrito = request.session.get('carrito', {})
    total_items = sum(item['cantidad'] for item in carrito.values())
    
    # Marcamos la categoría activa
    current_category = 'agua'
    
    return render(request, 'agua_catalogo.html', {
        'bidones': bidones,
        'total_items': total_items,
        'current_category': current_category
    })

from django.contrib.auth import login
from .forms import RegistroForm

def registro(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()  # Aquí es donde se guarda en la base de datos
            login(request, usuario)
            messages.success(request, "¡Registro exitoso!")
            return redirect('catalogo')
        else:
            # Si el formulario no es válido, esto imprimirá el motivo en tu terminal
            print(form.errors) 
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})