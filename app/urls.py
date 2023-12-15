
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("app/", views.index, name="app"),

    # PACIENTES CRUD
    path("pacientes/", views.pacientes, name="pacientes"),
    path("pacientes/create/", views.paciente_create, name="paciente_create"),
]
