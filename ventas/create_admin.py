from django.contrib.auth import get_user_model
import os
import django

# Configurar Django si se ejecuta como script independiente
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

# Cambia estos valores a tu gusto o usa variables de entorno
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'Amparo')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Amparo1234!')

# Crear superusuario solo si no existe
if not User.objects.filter(username=ADMIN_USERNAME).exists():
    print(f"Creando superusuario {ADMIN_USERNAME}...")
    User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email='',  # vacío, no hace falta
        password=ADMIN_PASSWORD
    )
    print("Superusuario creado.")
else:
    print("Superusuario ya existe.")
