from django import forms

from .models import (
    Paciente
)

class PacienteForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False  # Si deseas que el campo no sea obligatorio
    )
    
    class Meta:
        model = Paciente
        exclude = ("clinica",)