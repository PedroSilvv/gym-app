from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('gerar-treino/', views.criar_treino, name='criar-treino'),
    path('gerar-exercicios-random/', views.gerar_exercicios, name='gerar-exercicios')
]