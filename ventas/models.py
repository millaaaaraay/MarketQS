from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# --- MODELO PARA COMIDA DE MASCOTAS ---
class Alimento(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        return f"[Alimento] {self.marca} - {self.nombre}"

# --- MODELO PARA AGUA PURIFICA ---
class Bidon(models.Model):
    nombre = models.CharField(max_length=100) # Ej: Bidón 20 Litros
    precio = models.IntegerField()
    litros = models.DecimalField(max_digits=5, decimal_places=1)
    es_recarga = models.BooleanField(default=False) # Si es solo el agua o incluye envase
    stock = models.IntegerField(default=0)
    imagen_url = models.URLField(blank=True)

    def __str__(self):
        tipo = "Recarga" if self.es_recarga else "Envase Nuevo"
        return f"[Agua] {self.nombre} ({tipo})"

# --- EL CARRITO ---
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario}"

    @property
    def total_pagar(self):
        return sum(item.subtotal() for item in self.items.all())

# --- EL DETALLE DEL CARRITO (RELACIÓN GENÉRICA) ---
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    cantidad = models.PositiveIntegerField(default=1)

    # Configuración para que el item pueda ser Alimento O Bidon
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    producto = GenericForeignKey('content_type', 'object_id')

    def subtotal(self):
        # Accede al precio ya sea de Alimento o de Bidon
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"