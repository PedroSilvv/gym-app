from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('gerar-treino/', views.index, name='gerar-treino'),
]