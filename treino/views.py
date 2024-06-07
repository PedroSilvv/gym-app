from django.shortcuts import render, redirect, get_object_or_404
from .models import Treino, Exercicio, Serie, RESTRICOES_CHOICES, OBJETIVOS_CHOICES
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import random
from .utils.treino_utils import filtrar_exercicios, determinar_series_repeticoes, gerar_treino_para_aluno
from user.models import Aluno, CustomUser

@login_required(login_url='/user/login/')
def criar_treino(request):
    if request.user.groups.filter(name='Admin').exists():
        if request.method == "GET":
            return render(request, "create_ex.html", context={
                "objetivos_list" : OBJETIVOS_CHOICES,
                "restricoes_list" : RESTRICOES_CHOICES
            })
        
        elif request.method == "POST":

            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            tipo = request.POST.get('tipo')
            nivel = request.POST.get('nivel')

            objetivos = request.POST.getlist('objetivos')
            restricoes = request.POST.getlist('restricoes')

            exercicio = Exercicio.objects.create(nome=nome, descricao=descricao, tipo=tipo, nivel=nivel)

            exercicio.set_objetivos(objetivos)
            exercicio.set_restricoes_list(restricoes)
            exercicio.save()

            return render(request, "admin_home.html", context={
                "msg" : "Exercicio criado com sucesso!"
            })
    else:
        return redirect('default_view')



@login_required(login_url='/user/login/')
def gerar_exercicios(request):

    if request.user.groups.filter(name='Admin').exists():
        TIPO_CHOICES = ['Cardiovascular', 'Definição', 'Força', 'Funcional', 'Hipertrofia', 'Resistencia', 'Terapeutico']
        NIVEL_CHOICES = ['Iniciante', 'Intermediario', 'Avançado']

        restricoes_options = [choice[0] for choice in RESTRICOES_CHOICES]
        objetivos_options = [choice[0] for choice in OBJETIVOS_CHOICES]

        def criar_exercicio(nome, descricao, tipo, nivel, objetivos, restricoes):
            exercicio = Exercicio(
                nome=nome,
                descricao=descricao,
                tipo=tipo,
                nivel=nivel,
                objetivos=objetivos,
                restricoes=restricoes
            )
            exercicio.save()
            return exercicio

        def generate_combinations(options, max_length):
            num_options = random.randint(1, max_length)
            selected_options = random.sample(options, num_options)
            return ','.join(selected_options)

        for i in range(1, 41):
            nome = f"Exercicio {i}"
            descricao = f"Descricao do exercicio {i}"
            tipo = random.choice(TIPO_CHOICES)
            nivel = random.choice(NIVEL_CHOICES)
            objetivos = generate_combinations(objetivos_options, 5)
            restricoes = generate_combinations(restricoes_options, 5)
            
            criar_exercicio(nome, descricao, tipo, nivel, objetivos, restricoes)

        exercicios = Exercicio.objects.all().values()
        exercicio_response = list(exercicios)
        
        return JsonResponse(exercicio_response, safe=False)
    else:
        return redirect('default_view')
        

    

def aluno_gerar_treino(request):
    user = request.user
    aluno = get_object_or_404(Aluno, user=user)

    try:
        gerar_treino_para_aluno(aluno)
        return redirect('default_view')
    except Exception as e:
        return HttpResponse(F'Erro : {e}')


def detalhe_treino(request, id):

    try:
        treino = Treino.objects.filter(id=id).first()
        aluno = Aluno.objects.filter(user=request.user).first()

        if treino == None:
            return HttpResponse("Não encontrado treino com esse id: ")
        
        if treino.aluno != aluno:
            return HttpResponse("Você não tem autorização para acessar esse treino!")

        return render(request, "treino_detail.html", context={
            "treino" : treino,
        })
    except Exception as e:
        return HttpResponse("Não encontrado treino com esse id: "+ e )


