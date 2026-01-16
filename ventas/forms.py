# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Requerido para recuperar la contraseña.")

    class Meta:
        model = User
        fields = ["username", "email"]