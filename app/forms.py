from django import forms

from .models import (
    Paciente, Clinica
)

class PacienteForm(forms.ModelForm):

    fecha_nacimiento = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False  # Si deseas que el campo no sea obligatorio
    )
    
    class Meta:
        model = Paciente
        exclude = ("clinica",)

class ClinicaForm(forms.ModelForm):

    class Meta:
        model = Clinica
        exclude = ("creada_por", )