import threading
from pathlib import Path

from pyswip import Prolog

_KB_PATH = Path(__file__).resolve().parent.parent / "kb" / "heart_failure.pl"

_prolog: Prolog | None = None
_lock = threading.Lock()

MAJOR_SYMPTOMS = [
    "edema_pulmonar_agudo",
    "cardiomegalia",
    "reflujo_hepatoyugular",
    "distension_venas_cuello",
    "disnea_paroxistica_nocturna",
    "rales",
    "galope_tercer_ruido",
]

MINOR_SYMPTOMS = [
    "edema_tobillos",
    "disnea_esfuerzo",
    "hepatomegalia",
    "tos_nocturna",
    "derrame_pleural",
    "taquicardia",
]


def _get_prolog() -> Prolog:
    global _prolog
    if _prolog is None:
        _prolog = Prolog()
        _prolog.consult(str(_KB_PATH))
    return _prolog


def diagnose(form_data: dict) -> dict:
    """
    Runs the Framingham decision tree against the provided form data.
    Returns a dict with keys: diagnostico, tipo_ic, coronariografia,
    framingham, mayores_count, menores_count.
    """
    with _lock:
        prolog = _get_prolog()

        active_symptoms = [s for s in MAJOR_SYMPTOMS + MINOR_SYMPTOMS if form_data.get(s)]
        for symptom in active_symptoms:
            prolog.assertz(f"presente({symptom})")

        if form_data.get("bnp_elevado"):
            prolog.assertz("bnp_elevado")
        if form_data.get("fevi_menor_50"):
            prolog.assertz("fevi_menor_50")
        if form_data.get("angina"):
            prolog.assertz("angina")

        try:
            framingham = bool(list(prolog.query("cumple_framingham")))

            diag_results = list(prolog.query("diagnostico(D)"))
            diagnostico = diag_results[0]["D"] if diag_results else "sin_datos"

            tipo_results = list(prolog.query("tipo_ic(T)"))
            tipo_ic = tipo_results[0]["T"] if tipo_results else None

            coronariografia = bool(list(prolog.query("requiere_coronariografia")))

            mayores = [s for s in MAJOR_SYMPTOMS if form_data.get(s)]
            menores = [s for s in MINOR_SYMPTOMS if form_data.get(s)]

        finally:
            list(prolog.query("retractall(presente(_))"))
            list(prolog.query("retractall(bnp_elevado)"))
            list(prolog.query("retractall(fevi_menor_50)"))
            list(prolog.query("retractall(angina)"))

        return {
            "framingham": framingham,
            "diagnostico": diagnostico,
            "tipo_ic": tipo_ic,
            "coronariografia": coronariografia,
            "mayores_count": len(mayores),
            "menores_count": len(menores),
        }
