from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    PacienteForm, ClinicaForm
)
from .models import (
    Paciente, Clinica
)
# Create your views here.

def landing(request):
    return render(request, 'landing.html')

@login_required
def select_clinica(request):
    clinicas = request.user.clinic_memberships.all()
    context = {
        "q": clinicas
    }
    return render(request, 'select_clinica.html', context)


@login_required
def index(request, id_clinica):
    context = {"id_clinica": id_clinica}
    return render(request, 'index.html', context)


@login_required
def pacientes(request, id_clinica):

    clinica = get_object_or_404(Clinica, id=id_clinica)

    q = clinica.obtener_pacientes()

    context = {
        "id_clinica": id_clinica,
        "q": q
    }
    
    return render(request, 'pacientes.html', context)

@login_required
def paciente_create(request, id_clinica):
    
    form = PacienteForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            form.instance.clinica = get_object_or_404(Clinica, id=id_clinica)
            producto = form.save()
            return redirect("pacientes", id_clinica=id_clinica)
        
    context = {
        "form": form,
        "id_clinica": id_clinica
    }

    return render(request, 'pacientes/create.html', context)

@login_required
def paciente_edit(request, paciente_id, id_clinica):
    
    clinica = get_object_or_404(Clinica, id=id_clinica)

    paciente = get_object_or_404(Paciente, id=paciente_id, clinica=clinica)

    form = PacienteForm(request.POST or None, request.FILES or None, instance=paciente)

    if request.method == "POST":

        if form.is_valid():
            form.instance.clinica = clinica
            form.save()
            return redirect("pacientes", id_clinica=id_clinica)
        
    context = {
        "form": form,
        "id_clinica": id_clinica,
    }

    return render(request, 'pacientes/create.html', context)

@login_required
def clinica_create(request):
    
    form = ClinicaForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            form.instance.creada_por = request.user
            clinica = form.save()
            return redirect("app", id_clinica=clinica.id)

    context = {
        "form": form
    }


    return render(request, 'clinicas/create.html', context)
    

@login_required
def paciente_view(request, paciente_id, id_clinica):
    
    clinica = get_object_or_404(Clinica, id=id_clinica)

    paciente = get_object_or_404(Paciente, id=paciente_id, clinica=clinica)

    #form = PacienteForm(request.POST or None, request.FILES or None, instance=paciente)

    if request.method == "POST":
        pass
        # if form.is_valid():
        #     form.instance.clinica = clinica
        #     form.save()
        #     return redirect("pacientes", id_clinica=id_clinica)
        
    context = {
      #  "form": form,
        "id_clinica": id_clinica,
        "obj": paciente
    }

    return render(request, 'pacientes/view.html', context)