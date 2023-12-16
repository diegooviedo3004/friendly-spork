
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("app/<int:id_clinica>", views.index, name="app"),


    path("select_clinica/", views.select_clinica, name="select_clinica"),


    # CLINICA CRUD
    path("clinica/create/", views.clinica_create, name="clinica_create"),

    # PACIENTES CRUD
    path("pacientes/<int:id_clinica>/", views.pacientes, name="pacientes"),
    path("pacientes/create/<int:id_clinica>/", views.paciente_create, name="paciente_create"),
    path("pacientes/edit/<int:paciente_id>/<int:id_clinica>/", views.paciente_edit, name="paciente_edit"),
]
