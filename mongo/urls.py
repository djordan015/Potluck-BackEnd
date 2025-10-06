from django.urls import path
from . import views

urlpatterns = [
    path("samples_list/", views.samples_list, name="samples_list"),
    path("", views.index, name="index"),
]
