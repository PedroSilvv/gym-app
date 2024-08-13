from django.shortcuts import render, redirect, get_object_or_404
from .models import Esporte, CustomUser, Aluno, LESOES_CHOICES, OBJETIVOS_CHOICES, OBSERVACOES_CHOICES
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import Group
from random import randint
from django.contrib.auth.decorators import login_required
from treino.models import Exercicio, Treino, Serie




@login_required(login_url='/user/login/')
def registrar_aluno(request):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "GET":
            return render(request, "register.html", context={
                "esportes" : Esporte.objects.all(),
                "lesoes_list" : LESOES_CHOICES,
                "objetivos_list" : OBJETIVOS_CHOICES,
                "observacoes_list" : OBSERVACOES_CHOICES, 
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

            #FIELDS SIMPLES
            peso = request.POST.get('peso')
            altura = request.POST.get('altura')
            experiencia = request.POST.get('experiencia')
            dias = request.POST.get('dias')
            #LIST FIELDS - ALUNO
            esporte_ids = request.POST.getlist('esportes')
            lesoes = request.POST.getlist('lesoes')
            objetivos = request.POST.getlist('objetivos')
            observacoes = request.POST.getlist('observacoes')

            #PASSANDO USER CRIADO PARA A INSTANCIA DE ALUNO E ADICIONANDO OUTROS CAMPOS
            aluno = Aluno.objects.create(user=user, peso=peso, altura=altura, experiencia=experiencia, dias_treino_semanal=dias )

            #ADICIONANDO CAMPOS QUE SAO LISTAS OU MANY TO MANY.
            for e in esporte_ids:
                aluno.esportes_praticados.add(e)

            aluno.set_lesoes(lesoes)
            aluno.set_objetivos(objetivos)
            aluno.set_observacoes(observacoes)
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
                return redirect('admin-home')
            else:
                return redirect('default_view')

        else:
            return redirect('login')



def default_view(request):

    if request.user.groups.filter(name='Default').exists():
        aluno = get_object_or_404(Aluno, user=request.user)
        print(Treino.objects.filter(aluno=aluno, concluido=False, aceitou=False).count())
        return render(request, "default.html", context={
            "user" : f"{request.user.nome}",
            "treinos" : Treino.objects.filter(aluno=aluno, concluido=False, aceitou=True),
            "treino_pendente" : Treino.objects.filter(aluno=aluno, concluido=False, aceitou=False).count()
        })
        
    else:
        return redirect('admin-home')
    

def admin_home(request):

    if request.user.groups.filter(name='Admin').exists():
        personal = request.user
        treinos_para_feedback = Treino.objects.filter(personal=personal, aceitou=False).order_by('-data') #aceitou=False

        return render(request, "admin_home.html", context={
            "notificacoes" : treinos_para_feedback,
            "mostrar_notificacoes" : True,
        })
    else:
        return redirect('default_view')


def alunos_list(request):
    if request.user.groups.filter(name='Admin').exists():
        personal = request.user
        alunos_list = Aluno.objects.all()
        return render(request, "alunos_list.html", context={
            "alunos" : alunos_list,
            "mostrar_notificacoes" : False,
        })
    else:
        return redirect('default_view')



def aluno_profile(request, id):

    aluno_user = CustomUser.objects.filter(id=id).first()
    aluno = get_object_or_404(Aluno, user=aluno_user)


    return render(request, "aluno_profile.html", context={
            "aluno" : f"{aluno.user.nome}",
            "treinos" : Treino.objects.filter(aluno=aluno, concluido=False, aceitou=True),
            "treino_pendente" : Treino.objects.filter(aluno=aluno, concluido=False, aceitou=False).count()
        })