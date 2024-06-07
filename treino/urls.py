from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('criar-treino/', views.criar_treino, name='criar-treino'),
    path('gerar-exercicios-random/', views.gerar_exercicios, name='gerar-exercicios'),
    path('aluno-gerar-treino/', views.aluno_gerar_treino, name='aluno-gerar-treino' ),
    path('detalhe-treino/<int:id>/', views.detalhe_treino, name='detalhe-treino'),
]