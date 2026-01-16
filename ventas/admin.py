from django.contrib import admin
from .models import Alimento, Bidon, Carrito, ItemCarrito

# --- CONFIGURACIÓN PARA ALIMENTOS ---
@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla principal
    list_display = ('id', 'marca', 'nombre', 'precio', 'stock')
    
    # El ID es el único que te lleva al detalle, permitiendo que el resto sea editable
    list_display_links = ('id',)
    
    # Permite editar estos campos directamente sin entrar al producto
    list_editable = ('marca', 'nombre', 'precio', 'stock')
    
    # Buscador por marca y nombre
    search_fields = ('marca', 'nombre')
    
    # Filtro lateral por marca
    list_filter = ('marca',)

# --- CONFIGURACIÓN PARA BIDONES (AGUA) ---
@admin.register(Bidon)
class BidonAdmin(admin.ModelAdmin):
    # Columnas específicas para el agua
    list_display = ('id', 'nombre', 'litros', 'precio', 'stock', 'es_recarga')
    
    list_display_links = ('id',)
    
    # Edición rápida de precios y stock de agua
    list_editable = ('nombre', 'precio', 'stock', 'es_recarga')
    
    # Filtro para ver rápidamente quiénes necesitan recarga
    list_filter = ('es_recarga', 'litros')
    
    search_fields = ('nombre',)

# --- CONFIGURACIÓN PARA EL CARRITO ---
# Usamos un TabularInline para ver los productos dentro del mismo carrito
class ItemCarritoInline(admin.TabularInline):
    model = ItemCarrito
    extra = 0 # No mostrar filas vacías extra
    readonly_fields = ('subtotal',) # Solo lectura para el cálculo

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'creado', 'total_pagar')
    inlines = [ItemCarritoInline] # Esto permite ver qué compraron dentro del carrito
    list_filter = ('creado',)
    search_fields = ('usuario__username',)

# También registramos ItemCarrito por si necesitas borrar algo específico
admin.site.register(ItemCarrito)