from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    PacienteForm, ClinicaForm, DiagnosticoPacienteForm
)
from .models import (
    Paciente, Clinica, CategoriaDiagnostico, Diagnostico
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

@login_required
def diagnostico_create(request, paciente_id, clinica_id):
    
    form = DiagnosticoPacienteForm(request.POST or None, request.FILES or None)
    paciente = get_object_or_404(Paciente, id=paciente_id, clinica__id=clinica_id)

    if request.method == "POST":

        if form.is_valid():
            form.instance.paciente = paciente
            diagnostico = form.save()
            return redirect("paciente_view", paciente_id=paciente_id, id_clinica=clinica_id)

    diagnosticos = Diagnostico.objects.all()

    context = {
        "form": form,
        "id_clinica": clinica_id,
        "diagnosticos": diagnosticos
    }


    return render(request, 'diagnostico/create.html', context)





# def create_data(request):


    DATA = {
     "ANEMIA": [
        {
            "codigo": "D460",
            "nombre": "ANEMIA REFRACTARIA SIN SIDEROBLASTOS, ASI DESCRITA"
        },
        {
            "codigo": "D51",
            "nombre": "ANEMIA POR DEFICIENCIA DE VITAMINA B12"
        },
        {
            "codigo": "D52",
            "nombre": "ANEMIA POR DEFICIENCIA DE FOLATOS"
        },
        {
            "codigo": "D53",
            "nombre": "OTRAS ANEMIAS NUTRICIONALES"
        },
        {
            "codigo": "D55",
            "nombre": "ANEMIA DEBIDA A TRASTORNOS ENZIMATICOS"
        },
        {
            "codigo": "D570",
            "nombre": "ANEMIA FALCIFORME CON CRISIS"
        },
        {
            "codigo": "D58",
            "nombre": "OTRAS ANEMIAS HEMOLITICAS HEREDITARIAS"
        },
        {
            "codigo": "D59",
            "nombre": "ANEMIA HEMOLITICA ADQUIRIDA"
        },
        {
            "codigo": "D61",
            "nombre": "OTRAS ANEMIAS APLASTICAS"
        },
        {
            "codigo": "D62",
            "nombre": "ANEMIA POSTHEMORRAGICA AGUDA"
        },
        {
            "codigo": "D63",
            "nombre": "ANEMIA EN ENFERMEDADES CRONICAS CLASIFICADAS EN OTRA PARTE"
        },
        {
            "codigo": "D64",
            "nombre": "OTRAS ANEMIAS"
        },
        {
            "codigo": "O990",
            "nombre": "ANEMIA QUE COMPLICA EL EMBARAZO, EL PARTO Y EL PUERPERIO"
        }
    ],
    "ANEURISMA": [
        {
            "codigo": "I253",
            "nombre": "ANEURISMA CARDIACO"
        },
        {
            "codigo": "I281",
            "nombre": "ANEURISMA DE LA ARTERIA PULMONAR"
        },
        {
            "codigo": "I671",
            "nombre": "ANEURISMA CEREBRAL, SIN RUPTURA"
        },
        {
            "codigo": "I71",
            "nombre": "ANEURISMA Y DISECCION AORTICOS"
        },
        {
            "codigo": "I72",
            "nombre": "OTROS ANEURISMAS"
        }
    ],
    "ARRITMIAS": [
        {
            "codigo": "I49",
            "nombre": "OTRAS ARRITMIAS CARDIACAS"
        },
        {
            "codigo": "I498",
            "nombre": "OTRAS ARRITMIAS CARDIACAS ESPECIFICADAS"
        }
    ],
    "ARTRITIS REUMATOIDEA": [
        {
            "codigo": "M058",
            "nombre": "OTRAS ARTRITIS REUMATOIDEAS SEROPOSITIVAS"
        },
        {
            "codigo": "M059",
            "nombre": "ARTRITIS REUMATOIDEA SEROPOSITIVA, SIN OTRA ESPECIFICACION"
        }
    ],
    "ARTROSIS": [
        {
            "codigo": "M124",
            "nombre": "HIDRARTROSIS INTERMITENTE"
        },
        {
            "codigo": "M15",
            "nombre": "POLIARTROSIS"
        },
        {
            "codigo": "M158",
            "nombre": "OTRAS POLIARTROSIS"
        },
        {
            "codigo": "M16",
            "nombre": "COXARTROSIS [ARTROSIS DE LA CADERA]"
        },
        {
            "codigo": "M17",
            "nombre": "GONARTROSIS [ARTROSIS DE LA RODILLA]"
        },
        {
            "codigo": "M179",
            "nombre": "GONARTROSIS, NO ESPECIFICADA"
        },
        {
            "codigo": "M18",
            "nombre": "ARTROSIS DE LA PRIMERA ARTICULACION CARPOMETACARPIANA"
        },
        {
            "codigo": "M19",
            "nombre": "OTRAS ARTROSIS"
        },
        {
            "codigo": "M250",
            "nombre": "HEMARTROSIS"
        },
        {
            "codigo": "M841",
            "nombre": "FALTA DE CONSOLIDACION DE FRACTURA [SEUDOARTROSIS]"
        },
        {
            "codigo": "M960",
            "nombre": "SEUDOARTROSIS CONSECUTIVA A FUSION O ARTRODESIS"
        }
    ],
    "ASTENIA": [
        {
            "codigo": "G933",
            "nombre": "SINDROME DE FATIGA POSTVIRAL"
        },
        {
            "codigo": "M484",
            "nombre": "FRACTURA DE VERTEBRA POR FATIGA"
        },
        {
            "codigo": "R53",
            "nombre": "MALESTAR Y FATIGA"
        },
        {
            "codigo": "T676",
            "nombre": "FATIGA POR CALOR, TRANSITORIA"
        }
    ],
    "DIABETES MELLITUS": [
        {"codigo": "E10", "nombre": "DIABETES MELLITUS INSULINODEPENDIENTE"},
        {"codigo": "E107", "nombre": "DIABETES MELLITUS INSULINODEPENDIENTE, CON COMPLICACIONES MULTIPLES"},
        {"codigo": "E108", "nombre": "DIABETES MELLITUS INSULINODEPENDIENTE, CON COMPLICACIONES NO ESPECIFICADAS"},
        {"codigo": "E11", "nombre": "DIABETES MELLITUS NO INSULINODEPENDIENTE"},
        {"codigo": "E117", "nombre": "DIABETES MELLITUS NO INSULINODEPENDIENTE, CON COMPLICACIONES MULTIPLES"},
        {"codigo": "E118", "nombre": "DIABETES MELLITUS NO INSULINODEPENDIENTE, CON COMPLICACIONES NO ESPECIFICAD"},
        {"codigo": "E12", "nombre": "DIABETES MELLITUS ASOCIADA CON DESNUTRICION"},
        {"codigo": "E13", "nombre": "OTRAS DIABETES MELLITUS ESPECIFICADAS"},
        {"codigo": "E14", "nombre": "DIABETES MELLITUS, NO ESPECIFICADA"},
        {"codigo": "E232", "nombre": "DIABETES INSIPIDA"},
        {"codigo": "O240", "nombre": "DIABETES MELLITUS PREEXISTENTE INSULINODEPENDIENTE, EN EL EMBARAZO"},
        {"codigo": "O241", "nombre": "DIABETES MELLITUS PREEXISTENTE NO INSULINODEPENDIENTE, EN EL EMBARAZO"},
        {"codigo": "P700", "nombre": "SINDROME DEL RECIEN NACIDO DE MADRE CON DIABETES GESTACIONAL"},
        {"codigo": "Z131", "nombre": "EXAMEN DE PESQUISA ESPECIAL PARA DIABETES MELLITUS"},
        {"codigo": "Z833", "nombre": "HISTORIA FAMILIAR DE DIABETES MELLITUS"}
    ],
    "DIARREA": [
        {"codigo": "A09", "nombre": "DIARREA Y GASTROENTERITIS DE PRESUNTO ORIGEN INFECCIOSO"},
        {"codigo": "K580", "nombre": "SINDROME DEL COLON IRRITABLE CON DIARREA"},
        {"codigo": "K591", "nombre": "DIARREA FUNCIONAL"},
        {"codigo": "P783", "nombre": "DIARREA NEONATAL NO INFECCIOSA"}
    ],
    "ENFERMEDAD DE HODGKIN": [
        {"codigo": "C81", "nombre": "ENFERMEDAD DE HODGKIN"},
        {"codigo": "B212", "nombre": "ENFERMEDAD POR VIH, RESULTANTE EN OTROS TIPOS DE LINFOMA NO HODGKIN"},
        {"codigo": "C817", "nombre": "OTROS TIPOS DE ENFERMEDAD DE HODGKIN"},
        {"codigo": "C819", "nombre": "ENFERMEDAD DE HODGKIN, NO ESPECIFICADA"},
        {"codigo": "C82", "nombre": "LINFOMA NO HODGKIN FOLICULAR [NODULAR]"},
        {"codigo": "C83", "nombre": "LINFOMA NO HODGKIN DIFUSO"},
        {"codigo": "C85", "nombre": "LINFOMA NO HODGKIN DE OTRO TIPO Y EL NO ESPECIFICADO"}
    ],
    "ESCABIOSIS": [
        {"codigo": "B86", "nombre": "ESCABIOSIS"}
    ],
    "FARINGITIS": [
        {"codigo": "A545", "nombre": "FARINGITIS GONOCOCICA"},
        {"codigo": "B085", "nombre": "FARINGITIS VESICULAR ENTEROVIRICA"},
        {"codigo": "J00", "nombre": "RINOFARINGITIS AGUDA [RESFRIADO COMUN]"},
        {"codigo": "J02", "nombre": "FARINGITIS AGUDA"},
        {"codigo": "J020", "nombre": "FARINGITIS ESTREPTOCOCICA"},
        {"codigo": "J060", "nombre": "LARINGOFARINGITIS AGUDA"},
        {"codigo": "J31", "nombre": "RINITIS, RINOFARINGITIS Y FARINGITIS CRONICAS"},
        {"codigo": "J312", "nombre": "FARINGITIS CRONICA"}
    ],
    "FIBROSIS QUISTICA": [
        {"codigo": "E84", "nombre": "FIBROSIS QUISTICA"},
        {"codigo": "E840", "nombre": "FIBROSIS QUISTICA CON MANIFESTACIONES PULMONARES"},
        {"codigo": "E841", "nombre": "FIBROSIS QUISTICA CON MANIFESTACIONES INTESTINALES"}
    ],
    "FIEBRE": [
        {"codigo": "A68", "nombre": "FIEBRES RECURRENTES"},
        {"codigo": "A78", "nombre": "FIEBRE Q"},
        {"codigo": "R50", "nombre": "FIEBRE DE ORIGEN DESCONOCIDO"},
        {"codigo": "R500", "nombre": "FIEBRE CON ESCALOFRIO"},
        {"codigo": "R501", "nombre": "FIEBRE PERSISTENTE"},
        {"codigo": "A01", "nombre": "FIEBRES TIFOIDEA Y PARATIFOIDEA"},
        {"codigo": "A93", "nombre": "OTRAS FIEBRES VIRALES TRANSMITIDAS POR ARTROPODOS, NO CLASIFICADAS EN OTRA"},
        {"codigo": "A95", "nombre": "FIEBRE AMARILLA"},
        {"codigo": "A960", "nombre": "FIEBRE HEMORRAGICA DE JUNIN"}
    ],
    "FIEBRE REUMÁTICA": [
        {"codigo": "I00", "nombre": "FIEBRE REUMATICA SIN MENCION DE COMPLICACION CARDIACA"},
        {"codigo": "I01", "nombre": "FIEBRE REUMATICA CON COMPLICACION CARDIACA"},
        {"codigo": "L540", "nombre": "ERITEMA MARGINADO EN LA FIEBRE REUMATICA AGUDA (I00+)"}
    ],
    "GASTROENTERITIS": [
        {"codigo": "A09", "nombre": "DIARREA Y GASTROENTERITIS DE PRESUNTO ORIGEN INFECCIOSO"},
        {"codigo": "K52", "nombre": "OTRAS COLITIS Y GASTROENTERITIS NO INFECCIOSAS"},
        {"codigo": "K520", "nombre": "COLITIS Y GASTROENTERITIS DEBIDAS A RADIACION"},
        {"codigo": "K521", "nombre": "COLITIS Y GASTROENTERITIS TOXICAS"},
        {"codigo": "K522", "nombre": "COLITIS Y GASTROENTERITIS ALERGICAS Y DIETETICAS"},
        {"codigo": "K529", "nombre": "COLITIS Y GASTROENTERITIS NO INFECCIOSAS, NO ESPECIFICADAS"},
        {"codigo": "K50", "nombre": "ENFERMEDAD DE CROHN [ENTERITIS REGIONAL]"},
        {"codigo": "A083", "nombre": "OTRAS ENTERITIS VIRALES"}
    ],
    "HEMATURIA": [
        {"codigo": "R31", "nombre": "HEMATURIA, NO ESPECIFICADA"},
        {"codigo": "N02", "nombre": "HEMATURIA RECURRENTE Y PERSISTENTE"}
    ],
     "HEPATITIS": [
        {"codigo": "B15", "nombre": "HEPATITIS AGUDA TIPO A"},
        {"codigo": "B16", "nombre": "HEPATITIS AGUDA TIPO B"},
        {"codigo": "B17", "nombre": "OTRAS HEPATITIS VIRALES AGUDAS"},
        {"codigo": "B171", "nombre": "HEPATITIS AGUDA TIPO C"},
        {"codigo": "B172", "nombre": "HEPATITIS AGUDA TIPO E"},
        {"codigo": "B18", "nombre": "HEPATITIS VIRAL CRONICA"},
        {"codigo": "B19", "nombre": "HEPATITIS VIRAL, SIN OTRA ESPECIFICACION"},
        {"codigo": "B942", "nombre": "SECUELAS DE HEPATITIS VIRAL"},
        {"codigo": "K701", "nombre": "HEPATITIS ALCOHOLICA"},
        {"codigo": "K712", "nombre": "ENFERMEDAD TOXICA DEL HIGADO CON HEPATITIS AGUDA"},
        {"codigo": "K713", "nombre": "ENFERMEDAD TOXICA DEL HIGADO CON HEPATITIS CRONICA PERSISTENTE"},
        {"codigo": "K73", "nombre": "HEPATITIS CRONICA, NO CLASIFICADA EN OTRA PARTE"},
        {"codigo": "K752", "nombre": "HEPATITIS REACTIVA NO ESPECIFICA"},
        {"codigo": "O984", "nombre": "HEPATITIS VIRAL QUE COMPLICA EL EMBARAZO, EL PARTO Y EL PUERPERIO"},
        {"codigo": "P353", "nombre": "HEPATITIS VIRAL CONGENITA"},
        {"codigo": "Z205", "nombre": "CONTACTO CON Y EXPOSICION A HEPATITIS VIRAL"},
        {"codigo": "Z225", "nombre": "PORTADOR DE HEPATITIS VIRAL"},
        {"codigo": "Z246", "nombre": "NECESIDAD DE INMUNIZACION CONTRA LA HEPATITIS VIRAL"}
    ],
    "HERPES": [
        {"codigo": "A60", "nombre": "INFECCION ANOGENITAL DEBIDA A VIRUS DEL HERPES [HERPES SIMPLE]"},
        {"codigo": "B00", "nombre": "INFECCIONES HERPETICAS [HERPES SIMPLE]"},
        {"codigo": "B02", "nombre": "HERPES ZOSTER"},
        {"codigo": "B028", "nombre": "HERPES ZOSTER CON OTRAS COMPLICACIONES"},
        {"codigo": "B029", "nombre": "HERPES ZOSTER SIN COMPLICACIONES"},
        {"codigo": "B270", "nombre": "MONONUCLEOSIS DEBIDA A HERPES VIRUS GAMMA"},
        {"codigo": "G530", "nombre": "NEURALGIA POSTHERPES ZOSTER (B02.2+)"},
        {"codigo": "H191", "nombre": "QUERATITIS Y QUERATOCONJUNTIVITIS POR HERPES SIMPLE (B00.5+)"},
        {"codigo": "O264", "nombre": "HERPES GESTACIONAL"},
        {"codigo": "P352", "nombre": "INFECCIONES CONGENITAS POR VIRUS DEL HERPES SIMPLE"}
    ],
    "LINFOMA NO-HODGKIN": [
        {"codigo": "C85", "nombre": "LINFOMA NO HODGKIN DE OTRO TIPO Y EL NO ESPECIFICADO"},
        {"codigo": "C83", "nombre": "LINFOMA NO HODGKIN DIFUSO"},
        {"codigo": "C82", "nombre": "LINFOMA NO HODGKIN FOLICULAR [NODULAR]"},
        {"codigo": "C84", "nombre": "LINFOMA DE CELULAS T, PERIFERICO Y CUTANEO"},
        {"codigo": "L412", "nombre": "PAPULOSIS LINFOMATOIDE"}
    ],
    "MAREOS": [
        {"codigo": "H811", "nombre": "VERTIGO PAROXISTICO BENIGNO"}
    ],
    "MELANOMA": [
        {"codigo": "C43", "nombre": "MELANOMA MALIGNO DE LA PIEL"},
        {"codigo": "D03", "nombre": "MELANOMA IN SITU"}
    ],
    "MIELOMA": [
        {"codigo": "C900", "nombre": "MIELOMA MULTIPLE"},
        {"codigo": "M820", "nombre": "OSTEOPOROSIS EN MIELOMATOSIS MULTIPLE (C90.0+)"}
    ],
    "MONONUCLEOSIS Y LA INFECCIOSA": [
        {"codigo": "B27", "nombre": "MONONUCLEOSIS INFECCIOSA"},
        {"codigo": "B270", "nombre": "MONONUCLEOSIS DEBIDA A HERPES VIRUS GAMMA"},
        {"codigo": "B271", "nombre": "MONONUCLEOSIS POR CITOMEGALOVIRUS"}
    ],
    "OBESIDAD": [
        {"codigo": "E66", "nombre": "OBESIDAD"}
    ],
    "PAROTIDITIS": [
        {"codigo": "B26", "nombre": "PAROTIDITIS INFECCIOSA"},
        {"codigo": "B268", "nombre": "PAROTIDITIS INFECCIOSA CON OTRAS COMPLICACIONES"},
        {"codigo": "B269", "nombre": "PAROTIDITIS, SIN COMPLICACIONES"},
        {"codigo": "Z250", "nombre": "NECESIDAD DE INMUNIZACION SOLO CONTRA LA PAROTIDITIS"}
    ],
    "POLIARTRALGIAS": [
        {"codigo": "M25", "nombre": "OTROS TRASTORNOS ARTICULARES, NO CLASIFICADOS EN OTRA PARTE"},
        {"codigo": "M245", "nombre": "CONTRACTURA ARTICULAR"},
        {"codigo": "M253", "nombre": "OTRAS INESTABILIDADES ARTICULARES"},
        {"codigo": "M259", "nombre": "TRASTORNO ARTICULAR, NO ESPECIFICADO"}
    ],
    "SARCOMA": [
        {"codigo": "C46", "nombre": "SARCOMA DE KAPOSI"},
        {"codigo": "C850", "nombre": "LINFOSARCOMA"},
        {"codigo": "C923", "nombre": "SARCOMA MIELOIDE"}
    ],
    "SINUSITIS": [
        {"codigo": "J01", "nombre": "SINUSITIS AGUDA"},
        {"codigo": "J32", "nombre": "SINUSITIS CRONICA"}
    ],
    "ANOREXIA": [
        {"codigo": "R630", "nombre": "ANOREXIA"}
    ],
    "EPILEPSIA": [
        {"codigo": "G40", "nombre": "EPILEPSIA"},
        {"codigo": "F803", "nombre": "AFASIA ADQUIRIDA CON EPILEPSIA [LANDAU-KLEFFNER]"},
        {"codigo": "Z820", "nombre": "HISTORIA FAMILIAR DE EPILEPSIA Y OTRAS ENFERMEDADES DEL SISTEMA NERVIOSO"}
    ],
    "INSUFICIENCIA CARDÍACA": [
        {"codigo": "I50", "nombre": "INSUFICIENCIA CARDIACA"},
        {"codigo": "P290", "nombre": "INSUFICIENCIA CARDIACA NEONATAL"}
    ],
    "RINOFARINGITIS": [
        {"codigo": "J00", "nombre": "RINOFARINGITIS AGUDA [RESFRIADO COMUN]"},
        {"codigo": "J311", "nombre": "RINOFARINGITIS CRONICA"}
    ],
    "AMIGDALITIS": [
        {"codigo": "J03", "nombre": "AMIGDALITIS AGUDA"},
        {"codigo": "J350", "nombre": "AMIGDALITIS CRONICA"}
    ],
    "BRONQUITIS OBSTRUCTIVA": [
        {"codigo": "J80", "nombre": "SINDROME DE DIFICULTAD RESPIRATORIA DEL ADULTO"},
        {"codigo": "J96", "nombre": "INSUFICIENCIA RESPIRATORIA, NO CLASIFICADA EN OTRA PARTE"}
    ],
    "T17 CUERPO EXTRANIO EN LAS VIAS RESPIRATORIAS": [
        {"codigo": "T17", "nombre": "CUERPO EXTRANIO EN LAS VIAS RESPIRATORIAS"}
    ],
    "RINITIS": [
        {"codigo": "J30", "nombre": "RINITIS ALERGICA Y VASOMOTORA"},
        {"codigo": "J31", "nombre": "RINITIS, RINOFARINGITIS Y FARINGITIS CRONICAS"},
        {"codigo": "J310", "nombre": "RINITIS CRONICA"}
    ],
    "ASMA": [
        {"codigo": "J45", "nombre": "ASMA"},
        {"codigo": "J450", "nombre": "ASMA PREDOMINANTEMENTE ALERGICA"},
        {"codigo": "J451", "nombre": "ASMA NO ALERGICA"}
    ],
     "ULCERA GASTRICA / DUODENAL": [
        {"codigo": "K25", "nombre": "ULCERA GASTRICA"},
        {"codigo": "K26", "nombre": "ULCERA DUODENAL"},
        {"codigo": "K27", "nombre": "ULCERA PEPTICA, DE SITIO NO ESPECIFICADO"},
        {"codigo": "K28", "nombre": "ULCERA GASTROYEYUNAL"}
    ],
    "GASTRITIS / DUODENETIS": [
        {"codigo": "K29", "nombre": "GASTRITIS Y DUODENITIS"},
        {"codigo": "K291", "nombre": "OTRAS GASTRITIS AGUDAS"},
        {"codigo": "K295", "nombre": "GASTRITIS CRONICA, NO ESPECIFICADA"}
    ],
    "DISPEPSIA": [
        {"codigo": "K30", "nombre": "DISPEPSIA"}
    ],
    "APENDICITIS": [
        {"codigo": "K35", "nombre": "APENDICITIS AGUDA"},
        {"codigo": "K350", "nombre": "APENDICITIS AGUDA CON PERITONITIS GENERALIZADA"}
    ],
    "CIRROSIS": [
        {"codigo": "K703", "nombre": "CIRROSIS HEPATICA ALCOHOLICA"},
        {"codigo": "K74", "nombre": "FIBROSIS Y CIRROSIS DEL HIGADO"}
    ],
    "COLELITIASIS": [
        {"codigo": "K80", "nombre": "COLELITIASIS"}
    ],
    "PSORIASIS": [
        {"codigo": "L40", "nombre": "PSORIASIS"},
        {"codigo": "L41", "nombre": "PARAPSORIASIS"},
        {"codigo": "M090", "nombre": "ARTRITIS JUVENIL EN LA PSORIASIS (L40.5+)"}
    ],
    "URTICARIA": [
        {"codigo": "L50", "nombre": "URTICARIA"}
    ],
    "ALOPECIA": [
        {"codigo": "L63", "nombre": "ALOPECIA AREATA"},
        {"codigo": "Q840", "nombre": "ALOPECIA CONGENITA"}
    ],
    "LUPUS ERITEMATOSO": [
        {"codigo": "L93", "nombre": "LUPUS ERITEMATOSO"},
        {"codigo": "M32", "nombre": "LUPUS ERITEMATOSO SISTEMICO"}
    ],
    "COLICO RENAL": [
        {"codigo": "N23", "nombre": "COLICO RENAL, NO ESPECIFICADO"}
    ],
    "ECLAMPSIA": [
        {"codigo": "O15", "nombre": "ECLAMPSIA"},
        {"codigo": "O149", "nombre": "PREECLAMPSIA, NO ESPECIFICADA"}
    ],
    "REACCION ALERGICA": [
        {"codigo": "T784", "nombre": "ALERGIA NO ESPECIFICADA"},
        {"codigo": "Z88", "nombre": "HISTORIA PERSONAL DE ALERGIA A DROGAS, MEDICAMENTOS Y SUSTANCIAS BIOLOGICAS"},
        {"codigo": "Z910", "nombre": "HISTORIA PERSONAL DE ALERGIA, NO DEBIDA A DROGAS NI A SUSTANCIAS BIOLOGICAS"}
    ],
    "CEFALEA": [
        {"codigo": "R51", "nombre": "CEFALEA"},
        {"codigo": "G44", "nombre": "OTROS SINDROMES DE CEFALEA"}
    ],
    "DISLIPEMIA": [
        {"codigo": "E756", "nombre": "TRASTORNO DEL ALMACENAMIENTO DE LIPIDOS, NO ESPECIFICADO"}
    ],
    "HIPERCOLESTEROLEMIA / COLESTEROLEMIA": [
        {"codigo": "E780", "nombre": "HIPERCOLESTEROLEMIA PURA"}
    ],
    "CLIMATERIO": [
        {"codigo": "N91", "nombre": "MENSTRUACION AUSENTE, ESCASA O RARA"},
        {"codigo": "N926", "nombre": "MENSTRUACION IRREGULAR, NO ESPECIFICADA"}
    ],
     "MENOPAUSIA": [
        {"codigo": "N953", "nombre": "ESTADOS ASOCIADOS CON MENOPAUSIA ARTIFICIAL"}
    ],
    "AMENORREA": [
        {"codigo": "N912", "nombre": "AMENORREA, SIN OTRA ESPECIFICACION"},
        {"codigo": "N910", "nombre": "AMENORREA PRIMARIA"},
        {"codigo": "N911", "nombre": "AMENORREA SECUNDARIA"}
    ],
    "LIPOTIMIA": [
        {"codigo": "R42", "nombre": "MAREO Y DESVANECIMIENTO"}
    ],
    "HIPOGONADISMO MASCULINO": [
        {"codigo": "T386", "nombre": "ANTIGONADOTROFINAS, ANTIESTROGENOS Y ANTIANDROGENOS, NO CLASIFICADOS EN OTR"}
    ],
    "DOLOR ABDOMINAL": [
        {"codigo": "R10", "nombre": "DOLOR ABDOMINAL Y PELVICO"}
    ],
    "CONSTIPACIÓN": [
        {"codigo": "K590", "nombre": "CONSTIPACION"}
    ],
    "SUDORACIÓN": [
        {"codigo": "L74", "nombre": "TRASTORNOS SUDORIPAROS ECRINOS"},
        {"codigo": "L75", "nombre": "TRASTORNOS SUDORIPAROS APOCRINOS"}
    ],
    "PREQUIRURGICO": [
        {"codigo": "Y838", "nombre": "OTROS PROCEDIMIENTOS QUIRURGICOS"}
    ],
    "INFECCION URINARIA": [
        {"codigo": "N390", "nombre": "INFECCION DE VIAS URINARIAS, SITIO NO ESPECIFICADO"},
        {"codigo": "O23", "nombre": "INFECCION DE LAS VIAS GENITOURINARIAS EN EL EMBARAZO"}
    ],
    "RAYNAUD, ENFERMEDAD - SINDROME": [
        {"codigo": "I730", "nombre": "SINDROME DE RAYNAUD"}
    ],
    "INFERTILIDAD MASCULINA": [
        {"codigo": "N484", "nombre": "IMPOTENCIA DE ORIGEN ORGANICO"}
    ],
    "MEGACOLON": [
        {"codigo": "K593", "nombre": "MEGACOLON, NO CLASIFICADO EN OTRA PARTE"},
        {"codigo": "K931", "nombre": "MEGACOLON EN LA ENFERMEDAD DE CHAGAS (B57.3+)"}
    ],
    "SINDROME FEBRIL PROLONGADO": [
        {"codigo": "R501", "nombre": "FIEBRE PERSISTENTE"}
    ],
    "SINDROME DE LA SILLA TURCA": [
        {"codigo": "M899", "nombre": "TRASTORNO DEL HUESO, NO ESPECIFICADO"}
    ],
    "LUMBALGIA": [
        {"codigo": "M545", "nombre": "LUMBAGO NO ESPECIFICADO"},
        {"codigo": "M544", "nombre": "LUMBAGO CON CIATICA"}
    ],
    "ABDOMEN AGUDO": [
        {"codigo": "R100", "nombre": "ABDOMEN AGUDO"}
    ],
    "ACV ISQUEMICO": [
        {"codigo": "I67", "nombre": "OTRAS ENFERMEDADES CEREBROVASCULARES"}
    ],
     "ANGOR": [
        {"codigo": "I20", "nombre": "ANGINA DE PECHO"},
        {"codigo": "I201", "nombre": "ANGINA DE PECHO CON ESPASMO DOCUMENTADO"}
    ],
    "BOCIO": [
        {"codigo": "E010", "nombre": "BOCIO DIFUSO (ENDEMICO) RELACIONADO CON DEFICIENCIA DE YODO"},
        {"codigo": "E011", "nombre": "BOCIO MULTINODULAR (ENDEMICO) RELACIONADO CON DEFICIENCIA DE YODO"},
        {"codigo": "E030", "nombre": "HIPOTIROIDISMO CONGENITO CON BOCIO DIFUSO"},
        {"codigo": "E04", "nombre": "OTRO BOCIO NO TOXICO"},
        {"codigo": "P720", "nombre": "BOCIO NEONATAL, NO CLASIFICADO EN OTRA PARTE"}
    ],
    "CONTROL DE CA.": [
        {"codigo": "Z08", "nombre": "EXAMEN DE SEGUIMIENTO CONSECUTIVO AL TRATAMIENTO POR TUMOR MALIGNO"}
    ],
    "DERMATITIS": [
        {"codigo": "L20", "nombre": "DERMATITIS ATOPICA"},
        {"codigo": "L23", "nombre": "DERMATITIS ALERGICA DE CONTACTO"},
        {"codigo": "L24", "nombre": "DERMATITIS DE CONTACTO POR IRRITANTES"},
        {"codigo": "L26", "nombre": "DERMATITIS EXFOLIATIVA"},
        {"codigo": "L30", "nombre": "OTRAS DERMATITIS"}
    ],
    "DISNEA": [
        {"codigo": "R060", "nombre": "DISNEA"}
    ],
    "DISURIA": [
        {"codigo": "R300", "nombre": "DISURIA"}
    ],
    "EPISTAXIS": [
        {"codigo": "R040", "nombre": "EPISTAXIS"}
    ],
    "HEPATOMEGALIA": [
        {"codigo": "R160", "nombre": "HEPATOMEGALIA, NO CLASIFICADA EN OTRA PARTE"},
        {"codigo": "R16", "nombre": "HEPATOMEGALIA Y ESPLENOMEGALIA, NO CLASIFICADAS EN OTRA PARTE"}
    ],
    "HEPATOPATIA": [
        {"codigo": "K75", "nombre": "OTRAS ENFERMEDADES INFLAMATORIAS DEL HIGADO"},
        {"codigo": "K76", "nombre": "OTRAS ENFERMEDADES DEL HIGADO"}
    ],
    "INFERTILIDAD FEMENINA": [
        {"codigo": "N97", "nombre": "INFERTILIDAD FEMENINA"}
    ],
    "INTOXICACION": [
        {"codigo": "A05", "nombre": "OTRAS INTOXICACIONES ALIMENTARIAS BACTERIANAS"},
        {"codigo": "Y91", "nombre": "EVIDENCIA DE ALCOHOLISMO DETERMINADA POR EL NIVEL DE INTOXICACION"}
    ],
    "METRORRAGIA": [
        {"codigo": "N92", "nombre": "MENSTRUACION EXCESIVA, FRECUENTE E IRREGULAR"}
    ],
    "OSTEOPENIA": [
        {"codigo": "M892", "nombre": "OTROS TRASTORNOS DEL DESARROLLO Y CRECIMIENTO OSEO"}
    ],
    "OSTEOPOROSIS": [
        {"codigo": "M80", "nombre": "OSTEOPOROSIS CON FRACTURA PATOLOGICA"},
        {"codigo": "M81", "nombre": "OSTEOPOROSIS SIN FRACTURA PATOLOGICA"},
        {"codigo": "M82", "nombre": "OSTEOPOROSIS EN ENFERMEDADES CLASIFICADAS EN OTRA PARTE"}
    ],
    "PIELONEFRITIS": [
        {"codigo": "N110", "nombre": "PIELONEFRITIS CRONICA NO OBSTRUCTIVA ASOCIADA CON REFLUJO"},
        {"codigo": "N111", "nombre": "PIELONEFRITIS CRONICA OBSTRUCTIVA"}
    ],
    "PROSTATISMO": [
        {"codigo": "N41", "nombre": "ENFERMEDADES INFLAMATORIAS DE LA PROSTATA"},
        {"codigo": "N42", "nombre": "OTROS TRASTORNOS DE LA PROSTATA"},
        {"codigo": "N40", "nombre": "HIPERPLASIA DE LA PROSTATA"}
    ],
    "ADENOMEGALIA": [
        {"codigo": "R59", "nombre": "ADENOMEGALIA"}
    ],
    "SOBREPESO": [
        {"codigo": "E66", "nombre": "OBESIDAD"}
    ],
    "VOMITOS": [
        {"codigo": "R11", "nombre": "NAUSEA Y VOMITO"}
    ],
    "ABORTOS ESPONTANEOS": [
        {"codigo": "O03", "nombre": "ABORTO ESPONTANEO"}
    ],
    "ACNE": [
        {"codigo": "L70", "nombre": "ACNE"}
    ],
    "ALERGIA RESPIRATORIA": [
        {"codigo": "T784", "nombre": "ALERGIA NO ESPECIFICADA"}
    ],
    "ANAOVULACION": [
        {"codigo": "N970", "nombre": "INFERTILIDAD FEMENINA ASOCIADA CON FALTA DE OVULACION"}
    ],
    "ANGINA": [
        {"codigo": "I200", "nombre": "ANGINA INESTABLE"}
    ],
    "ARRITMIA": [
        {"codigo": "I49", "nombre": "OTRAS ARRITMIAS CARDIACAS"}
    ],
    "ARTRALGIA": [
        {"codigo": "M24", "nombre": "OTROS TRASTORNOS ARTICULARES ESPECIFICOS"}
    ],
    "BAJO PESO": [
        {"codigo": "R634", "nombre": "PERDIDA ANORMAL DE PESO"},
        {"codigo": "P050", "nombre": "BAJO PESO PARA LA EDAD GESTACIONAL"},
        {"codigo": "P071", "nombre": "OTRO PESO BAJO AL NACER"}
    ],
    "CONJUNTIVITIS": [
        {"codigo": "H10", "nombre": "CONJUNTIVITIS"},
        {"codigo": "H104", "nombre": "CONJUNTIVITIS CRONICA"},
        {"codigo": "B30", "nombre": "CONJUNTIVITIS VIRAL"},
        {"codigo": "H102", "nombre": "OTRAS CONJUNTIVITIS AGUDAS"}
    ],
    "CONTROL BY PASS": [
        {"codigo": "Z95", "nombre": "PRESENCIA DE IMPLANTES E INJERTOS CARDIOVASCULARES"}
    ],
    "DESNUTRICIÓN": [
        {"codigo": "E43", "nombre": "DESNUTRICION PROTEICOCALORICA SEVERA, NO ESPECIFICADA"},
        {"codigo": "O25", "nombre": "DESNUTRICION EN EL EMBARAZO"},
        {"codigo": "P05", "nombre": "RETARDO DEL CRECIMIENTO FETAL Y DESNUTRICION FETAL"}
    ],
    "ETILISMO": [
        {"codigo": "Y909", "nombre": "PRESENCIA DE ALCOHOL EN LA SANGRE, NIVEL NO ESPECIFICADO"},
        {"codigo": "Y919", "nombre": "ALCOHOLISMO, NIVEL DE INTOXICACION NO ESPECIFICADO"}
    ],
    "EDEMAS": [
        {"codigo": "R60", "nombre": "EDEMA, NO CLASIFICADO EN OTRA PARTE"},
        {"codigo": "R600", "nombre": "EDEMA LOCALIZADO"},
        {"codigo": "R601", "nombre": "EDEMA GENERALIZADO"}
    ],
    "ENFERMEDAD DE TRANS. SEXUAL": [
        {"codigo": "A64", "nombre": "ENFERMEDAD DE TRANSMISION SEXUAL NO ESPECIFICADA"}
    ],
    "EPOC - INSUFICIENCIA RESPIRATORIA": [
        {"codigo": "J98", "nombre": "OTROS TRASTORNOS RESPIRATORIOS"}
    ],
    "GOTA": [
        {"codigo": "M10", "nombre": "GOTA"}
    ],
    "HEMATOMAS": [
        {"codigo": "T810", "nombre": "HEMORRAGIA Y HEMATOMA QUE COMPLICAN UN PROCEDIMIENTO, NO CLASIFICADOS EN OT"}
    ],
    "HIRSUTISMO": [
        {"codigo": "L680", "nombre": "HIRSUTISMO"}
    ],
     "ICTERICIA": [
        {"codigo": "R17", "nombre": "ICTERICIA NO ESPECIFICADA"},
        {"codigo": "P58", "nombre": "ICTERICIA NEONATAL DEBIDA A OTRAS HEMOLISIS EXCESIVAS"},
        {"codigo": "P59", "nombre": "ICTERICIA NEONATAL POR OTRAS CAUSAS Y POR LAS NO ESPECIFICADAS"}
    ],
    "LEUCEMIA": [
        {"codigo": "C959", "nombre": "LEUCEMIA, NO ESPECIFICADA"},
        {"codigo": "C91", "nombre": "LEUCEMIA LINFOIDE"},
        {"codigo": "C92", "nombre": "LEUCEMIA MIELOIDE"},
        {"codigo": "C93", "nombre": "LEUCEMIA MONOCITICA"}
    ],
    "LINFOMA": [
        {"codigo": "C963", "nombre": "LINFOMA HISTIOCITICO VERDADERO"},
        {"codigo": "C859", "nombre": "LINFOMA NO HODGKIN, NO ESPECIFICADO"},
        {"codigo": "C84", "nombre": "LINFOMA DE CELULAS T, PERIFERICO Y CUTANEO"},
        {"codigo": "C83", "nombre": "LINFOMA NO HODGKIN DIFUSO"},
        {"codigo": "C82", "nombre": "LINFOMA NO HODGKIN FOLICULAR [NODULAR]"}
    ],
    "LITIASIS VESICULAR": [
        {"codigo": "K80", "nombre": "COLELITIASIS"}
    ],
    "METABOLOPATIA": [
        {"codigo": "E88", "nombre": "OTROS TRASTORNOS METABOLICOS"}
    ],
    "MIALGIA": [
        {"codigo": "M791", "nombre": "MIALGIA"}
    ],
    "NEUMOPATIA": [
        {"codigo": "J189", "nombre": "NEUMONIA, NO ESPECIFICADA"}
    ],
    "POLIDIPSIA": [
        {"codigo": "R631", "nombre": "POLIDIPSIA"}
    ],
    "PRECORDIALGIA - DOLOR PRECORDIAL": [
        {"codigo": "R072", "nombre": "DOLOR PRECORDIAL"}
    ],
    "PRURITO": [
        {"codigo": "L29", "nombre": "PRURITO"}
    ],
    "SINDROME VERTIGINOSO": [
        {"codigo": "H82", "nombre": "SINDROMES VERTIGINOSOS EN ENFERMEDADES CLASIFICADAS EN OTRA PARTE"},
        {"codigo": "A881", "nombre": "VERTIGO EPIDEMICO"},
        {"codigo": "H814", "nombre": "VERTIGO DE ORIGEN CENTRAL"}
    ],
    "TOS CRONICA": [
        {"codigo": "A379", "nombre": "TOS FERINA, NO ESPECIFICADA"}
    ],
    "SINDROME DE OVARIO POLIQUISTICO": [
        {"codigo": "E282", "nombre": "SINDROME DE OVARIO POLIQUISTICO"}
    ],
    "EMBARAZO - CONTROL 1ER. TRIMESTRE": [
        {"codigo": "Z34", "nombre": "SUPERVISION DE EMBARAZO NORMAL"}
    ],
    "EMBARAZO - CONTROL 2DO. TRIMESTRE": [
        {"codigo": "Z34", "nombre": "SUPERVISION DE EMBARAZO NORMAL"}
    ],
    "EMBARAZO - CONTROL 3ER. TRIMESTRE": [
        {"codigo": "Z34", "nombre": "SUPERVISION DE EMBARAZO NORMAL"}
    ]
    }

    for categoria, diagnosticos in DATA.items():
        # Aquí puedes crear la categoría si aún no existe
        # Por ejemplo: 
        categoria_obj, created = CategoriaDiagnostico.objects.get_or_create(nombre=categoria)
        
        for diagnostico in diagnosticos:
            codigo = diagnostico["codigo"]
            nombre = diagnostico["nombre"]
            
            # Aquí creas o recuperas el diagnóstico y lo asocías a la categoría correspondiente
            # Por ejemplo:
            Diagnostico.objects.get_or_create(codigo=codigo, nombre=nombre, categoria=categoria_obj)
            
            print(f"Categoría: {categoria}, Código: {codigo}, Nombre: {nombre}")

    return "DONE"