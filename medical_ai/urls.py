from django.urls import path

from .views import index, decision_tree, diagnosis

urlpatterns = [
    path("", index, name="medical_index"),
    path("arbol/", decision_tree, name="medical_tree"),
    path("diagnostico/", diagnosis, name="medical_diagnosis"),
]
