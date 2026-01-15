from django.contrib import admin
from .models import Alimento

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    # Definimos qué columnas se ven
    list_display = ('id', 'marca', 'nombre', 'descripcion', 'precio', 'stock')
    
    # Hacemos que el ID sea el link para entrar, liberando la Marca
    list_display_links = ('id',)
    
    # AHORA SÍ puedes poner la marca aquí para editarla
    list_editable = ('marca', 'nombre', 'descripcion', 'precio', 'stock')
    
    search_fields = ('marca', 'nombre')