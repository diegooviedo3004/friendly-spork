from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    PacienteForm
)
from .models import (
    Paciente, Clinica
)
# Create your views here.

def landing(request):
    return render(request, 'landing.html')

@login_required
def index(request):
    request.session['clinica_id'] = 1

    return render(request, 'index.html')


@login_required
def pacientes(request):

    clinica_id = int(request.session['clinica_id'])

    clinica = get_object_or_404(Clinica, id=clinica_id)

    q = clinica.obtener_pacientes()

    context = {
        "q": q
    }
    
    return render(request, 'pacientes.html', context)

@login_required
def paciente_create(request):
    
    form = PacienteForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            form.instance.clinica = get_object_or_404(Clinica, id=int(request.session['clinica_id']))
            form.save()
            return redirect("pacientes")
        
    context = {
        "form": form
    }

    return render(request, 'pacientes/create.html', context)