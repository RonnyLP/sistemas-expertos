from django import forms

DEPT_CHOICES = [
    ("AMAZONAS", "Amazonas"),
    ("ANCASH", "Áncash"),
    ("APURIMAC", "Apurímac"),
    ("AREQUIPA", "Arequipa"),
    ("AYACUCHO", "Ayacucho"),
    ("CAJAMARCA", "Cajamarca"),
    ("CALLAO", "Callao"),
    ("CUSCO", "Cusco"),
    ("HUANCAVELICA", "Huancavelica"),
    ("HUANUCO", "Huánuco"),
    ("ICA", "Ica"),
    ("JUNIN", "Junín"),
    ("LA LIBERTAD", "La Libertad"),
    ("LAMBAYEQUE", "Lambayeque"),
    ("LIMA", "Lima"),
    ("LORETO", "Loreto"),
    ("MADRE DE DIOS", "Madre de Dios"),
    ("MOQUEGUA", "Moquegua"),
    ("PASCO", "Pasco"),
    ("PIURA", "Piura"),
    ("PUNO", "Puno"),
    ("SAN MARTIN", "San Martín"),
    ("TACNA", "Tacna"),
    ("TUMBES", "Tumbes"),
    ("UCAYALI", "Ucayali"),
]

SEX_CHOICES = [
    ("MASCULINO", "Masculino"),
    ("FEMENINO", "Femenino"),
]


class DiabetesForm(forms.Form):

    departamento = forms.ChoiceField(
        choices=DEPT_CHOICES,
        label="Departamento",
    )

    edad = forms.IntegerField(
        label="Edad (años)",
        min_value=0,
        max_value=110,
    )

    sexo = forms.ChoiceField(
        choices=SEX_CHOICES,
        label="Sexo",
    )

    glucosa = forms.FloatField(
        label="Glucosa en sangre (mg/dL)",
        min_value=0,
    )

    colesterol = forms.FloatField(
        label="Colesterol total (mg/dL)",
        min_value=0,
    )
