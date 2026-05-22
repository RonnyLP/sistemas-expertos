from django.shortcuts import render

from .forms import PredictionForm
from .services.predictor import predict_survival


def predict_view(request):

    result = None

    if request.method == "POST":

        form = PredictionForm(request.POST)

        if form.is_valid():

            data = {
                "sex": form.cleaned_data["sex"],
                "age": form.cleaned_data["age"],
                "n_siblings_spouses":
                    form.cleaned_data["n_siblings_spouses"],
                "parch":
                    form.cleaned_data["parch"],
                "fare":
                    form.cleaned_data["fare"],
                "class":
                    form.cleaned_data["passenger_class"],
                "deck":
                    form.cleaned_data["deck"],
                "embark_town":
                    form.cleaned_data["embark_town"],
                "alone":
                    form.cleaned_data["alone"],
            }

            prediction = predict_survival(data)

            result = (
                "Sobrevive"
                if prediction >= 0.5
                else "No sobrevive"
            )

    else:
        form = PredictionForm()

    return render(
        request,
        "accidents_ai/form.html",
        {
            "form": form,
            "result": result
        }
    )
