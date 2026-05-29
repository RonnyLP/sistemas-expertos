from django.urls import path

from .views import predict_view, tree_image

urlpatterns = [
    path("", predict_view, name="dt_predict"),
    path("arbol.png", tree_image, name="dt_tree_image"),
]
