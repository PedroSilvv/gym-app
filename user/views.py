from django.shortcuts import render, redirect
from .models import Esporte, CustomUser, Aluno, LESOES_CHOICES
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import Group
from random import randint
from django.contrib.auth.decorators import login_required



@login_required(login_url='/user/login/')
def registrar_aluno(request):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "GET":
            return render(request, "register.html", context={
                "esportes" : Esporte.objects.all(),
                "lesoes_list" : LESOES_CHOICES
            })
        
        elif request.method == "POST": 
            
            #Criando o Usuario para o Aluno se autenticar
            nome = request.POST.get('nome')
            username = request.POST.get('matricula')
            password = request.POST.get('password')
            email = request.POST.get('email')
            role_nome = request.POST.get('role')

            nome_recortado = nome.split()

            user = CustomUser.objects.create_user(nome=nome, username=username, first_name=nome_recortado[0],
                                                  last_name=nome_recortado[-1] ,email=email, password=password)
            role = Group.objects.get(name=role_nome)
            user.groups.add(role)
            user.save()

            ##Criando Instancia de ALUNO
            esporte_ids = request.POST.getlist('esportes')
            lesoes = request.POST.getlist('lesoes')
            objetivos = request.POST.get('objetivos')
            peso = request.POST.get('peso')
            altura = request.POST.get('altura')
            experiencia = request.POST.get('experiencia')
            
            aluno = Aluno.objects.create(user=user, objetivos=objetivos, peso=peso, altura=altura, experiencia=experiencia )

            for e in esporte_ids:
                aluno.esportes_praticados.add(e)

            aluno.set_lesoes(lesoes)
            aluno.save()

            if user:
                return render(request, "admin_home.html", context={
                    "msg" : "CRIADO COM SUCESSO"
                })
            else:
                return render(request, "register.html", context={
                    "msg" : "ERRO AO CRIAR"
                })
    else:
        return redirect('default_view')


def login(request):
    
    if request.method == "GET":

        return render(request, "login.html")

    else:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            login_user(request, user)
            if user.groups.filter(name='Admin').exists():
                return render(request, "admin_home.html")
            else:
                return redirect('default_view')

        else:
            return redirect('login')



def default_view(request):
    return render(request, "default.html", context={
        "msg" : f"Olá, {request.user.username}"
    })