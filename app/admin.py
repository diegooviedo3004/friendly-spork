from django.contrib import admin
from .models import Paciente, Genero, Clinica, ClinicaMiembro
# Register your models here.
admin.site.register([Paciente, Genero, Clinica, ClinicaMiembro])