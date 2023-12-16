from django.db import models
from django.contrib.auth.models import User


TAMANO_EXPEDIENTE = 10
# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Genero(BaseModel):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pais(BaseModel):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


TIPO_SANGRE_CHOICES = [
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B-', 'B-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('B+', 'B+'),
]

class Clinica(BaseModel):
    nombre = models.CharField(max_length=50)
    img = models.ImageField(upload_to='clinicas/', null=True, blank=True)
    creada_por = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_clinics', null=True)
    
    def obtener_pacientes(self):
        return self.paciente_set.all()
    
class ClinicaMiembro(models.Model):
    ROLES = [
        ('Administrador', 'Administrator'),
        ('Médico', 'Médico'),
        ('Secretario', 'Secretario'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic_memberships')
    clinica = models.ForeignKey(Clinica, on_delete=models.CASCADE, related_name='memberships')
    rol = models.CharField(max_length=20, choices=ROLES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'clinica')  # Evita que un usuario se una a la misma clínica más de una vez

class Paciente(BaseModel):
    clinica = models.ForeignKey(Clinica, on_delete=models.SET_NULL, null=True, blank=True)
    nombres = models.CharField(max_length=50)
    apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True, blank=True)
    pais = models.ForeignKey(Pais, blank=True, null=True, on_delete=models.SET_NULL)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    img = models.ImageField(upload_to='pacientes/', null=True, blank=True)
    grupo_sanguineo = models.CharField(max_length=10, null=True, blank=True, choices=TIPO_SANGRE_CHOICES)
    notas = models.TextField(null=True, blank=True)

    telefono = models.CharField(max_length=50, null=True, blank=True)

    def get_expediente(self):
        return f"# {self.id:0{TAMANO_EXPEDIENTE}d}"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Clinica)
def create_clinica_miembro(sender, instance, created, **kwargs):
    if created:
        # Cuando se crea una instancia de Clinica, crea automáticamente una instancia de ClinicaMiembro
        ClinicaMiembro.objects.create(user=instance.creada_por, clinica=instance, rol='Administrador')