from django.shortcuts import render

from .forms import DiagnosisForm
from .services.prolog_engine import diagnose

DIAGNOSTICO_LABELS = {
    "ic_sospechada": ("IC Sospechada", "danger"),
    "sospecha_diastolica": ("Sospecha de IC Diastólica", "warning"),
    "ic_descartada": ("IC Descartada", "success"),
}

TIPO_IC_LABELS = {
    "sistolica": "IC Sistólica (FEVI reducida)",
    "diastolica": "IC Diastólica (FEVI preservada)",
}


_MAYOR_LIST = [
    "Edema pulmonar agudo",
    "Cardiomegalia (radiografía de tórax)",
    "Reflujo hepatoyugular",
    "Distensión de venas del cuello",
    "Disnea paroxística nocturna u ortopnea",
    "Rales (crepitantes)",
    "Galope por tercer ruido cardíaco",
]

_MENOR_LIST = [
    "Edema de tobillos",
    "Disnea de esfuerzo",
    "Hepatomegalia",
    "Tos nocturna",
    "Derrame pleural",
    "Taquicardia (> 120 lpm)",
]


def index(request):
    return render(request, "medical_ai/index.html", {
        "mayor_list": _MAYOR_LIST,
        "menor_list": _MENOR_LIST,
    })


def decision_tree(request):
    return render(request, "medical_ai/decision_tree.html")


def diagnosis(request):
    result = None

    if request.method == "POST":
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            raw = diagnose(form.cleaned_data)

            label, badge = DIAGNOSTICO_LABELS.get(
                raw["diagnostico"], (raw["diagnostico"], "secondary")
            )
            tipo_label = TIPO_IC_LABELS.get(raw["tipo_ic"]) if raw["tipo_ic"] else None

            result = {
                **raw,
                "diagnostico_label": label,
                "badge_class": badge,
                "tipo_ic_label": tipo_label,
            }
    else:
        form = DiagnosisForm()

    return render(
        request,
        "medical_ai/diagnosis.html",
        {"form": form, "result": result},
    )
