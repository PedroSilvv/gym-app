from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('criar-treino/', views.criar_treino, name='criar-treino'),
    path('gerar-exercicios-random/', views.gerar_exercicios, name='gerar-exercicios'),
    path('aluno-gerar-treino/', views.aluno_gerar_treino, name='aluno-gerar-treino' ),
    path('detalhe-treino/<int:id>/', views.detalhe_treino, name='detalhe-treino'),
    path('detalhe-exercicio/<int:serie_id>/<int:ex_id>/', views.detalhe_exercicio, name='detalhe-exercicio'),
    path('concluir-treino/<int:id>/', views.aluno_concluir_treino, name='concluir-treino'),
    path('aprovar-treino/<int:id>/', views.personal_aprovar_treino, name='aprovar-treino'),
]