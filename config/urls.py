from django.contrib import admin
from django.urls import path, include # Importante agregar 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ventas.urls')), # Esto conecta tu tienda
]



