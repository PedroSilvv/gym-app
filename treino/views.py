from django.shortcuts import render, redirect
from .models import Treino, Exercicio, Serie, RESTRICOES_CHOICES, OBJETIVOS_CHOICES
import random
from django.http import HttpResponse, JsonResponse

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




def gerar_exercicios(request):

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
        

    


