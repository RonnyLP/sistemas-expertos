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


def index(request):
    return render(request, "medical_ai/index.html")


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
