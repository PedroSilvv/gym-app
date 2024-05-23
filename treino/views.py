from django.shortcuts import render, redirect
from .models import Treino, Exercicio, Serie, RESTRICOES_CHOICES, OBJETIVOS_CHOICES


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




        

    


