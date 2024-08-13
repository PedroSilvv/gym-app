from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registrar-aluno/', views.registrar_aluno, name='registrar'),
    path('default/', views.default_view, name='default_view'),
    path('admin-home', views.admin_home, name='admin-home'),
    path('meus-alunos/', views.alunos_list, name='alunos-list'),
    path('aluno-profile/<int:id>/', views.aluno_profile, name='aluno-profile'),
]