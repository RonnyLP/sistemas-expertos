from pathlib import Path

from django.http import FileResponse, Http404
from django.shortcuts import render

from .forms import DiabetesForm
from .services.predictor import predict_severity

_RESULT_MAP = {
    "sin_complicacion": ("Sin Complicación", "emerald"),
    "con_complicacion": ("Con Complicación", "amber"),
    "otro_trastorno": ("Otro Trastorno", "slate"),
}

_TREE_PNG = Path(__file__).resolve().parent / "ml" / "tree.png"


def predict_view(request):

    result = None

    if request.method == "POST":
        form = DiabetesForm(request.POST)
        if form.is_valid():
            data = {
                "departamento": form.cleaned_data["departamento"],
                "edad": form.cleaned_data["edad"],
                "sexo": form.cleaned_data["sexo"],
                "glucosa": form.cleaned_data["glucosa"],
                "colesterol": form.cleaned_data["colesterol"],
            }
            clase, confianza = predict_severity(data)
            label, color = _RESULT_MAP.get(clase, (clase, "slate"))
            result = {
                "clase": clase,
                "label": label,
                "color": color,
                "confianza": round(confianza * 100, 1),
            }
    else:
        form = DiabetesForm()

    return render(
        request,
        "decision_tree/form.html",
        {"form": form, "result": result},
    )


def tree_image(request):
    if not _TREE_PNG.exists():
        raise Http404("Imagen del árbol no encontrada. Ejecute train_model.py primero.")
    return FileResponse(_TREE_PNG.open("rb"), content_type="image/png")
