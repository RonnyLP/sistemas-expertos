from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="/accidentes/", permanent=False)),

    path("admin/", admin.site.urls),

    path("accidentes/", include("accidents_ai.urls")),

    path("arbol-de-decision/", include("decision_tree.urls")),

    path("insuficiencia-cardiaca/", include("medical_ai.urls")),
]
