from django.urls import path
from . import views

urlpatterns = [
    path('foods/', views.getFoods),
    path('food/', views.getFood),
    path('addFood/', views.addFood),
    path('recipes/', views.getRecipes),
    path('addRecipe/', views.addRecipe),
    path('', views.getRecipes),
]