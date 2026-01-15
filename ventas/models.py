from django.conf import settings
from django.db import models


class Alimento(models.Model):  # La "A" debe ser mayúscula
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)
    imagen_url = models.URLField(blank=True) 

    def __str__(self):
        return f"{self.marca} - {self.nombre}"
    
class Carrito(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.alimento.precio * self.cantidad