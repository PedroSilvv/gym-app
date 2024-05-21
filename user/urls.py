from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registrar-aluno/', views.registrar_aluno, name='registrar'),
    path('default/', views.default_view, name='default_view')
]