from django import forms

_CB = forms.CheckboxInput(attrs={"class": "form-check-input"})


def _bool(label):
    return forms.BooleanField(
        required=False,
        label=label,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )


class DiagnosisForm(forms.Form):

    # --- Criterios Mayores ---
    edema_pulmonar_agudo = _bool("Edema pulmonar agudo")
    cardiomegalia = _bool("Cardiomegalia (radiografía)")
    reflujo_hepatoyugular = _bool("Reflujo hepatoyugular")
    distension_venas_cuello = _bool("Distensión de venas del cuello")
    disnea_paroxistica_nocturna = _bool(
        "Disnea paroxística nocturna u ortopnea")
    rales = _bool("Rales (crepitantes)")
    galope_tercer_ruido = _bool("Galope por tercer ruido cardíaco")

    # --- Criterios Menores ---
    edema_tobillos = _bool("Edema de tobillos")
    disnea_esfuerzo = _bool("Disnea de esfuerzo")
    hepatomegalia = _bool("Hepatomegalia")
    tos_nocturna = _bool("Tos nocturna")
    derrame_pleural = _bool("Derrame pleural")
    taquicardia = _bool("Taquicardia (> 120 lpm)")

    # --- Datos adicionales para el árbol de decisión ---
    bnp_elevado = _bool("BNP elevado")
    fevi_menor_50 = _bool("FEVI < 50 % (ecocardiografía)")
    angina = _bool("Angina o dolor torácico presente")
