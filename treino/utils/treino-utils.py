from ..models import Exercicio, Treino, Serie
from user.models import Aluno

def filtrar_exercicios(aluno):
    # Filtrar por exp do Aluno
    exercicios_adequados = Exercicio.objects.filter(nivel__in=[aluno.experiencia, 'Iniciante'])

    # Excluir exercícios de acordo com as lesões
    lesoes = aluno.get_lesoes_list()
    for lesao in lesoes:
        exercicios_adequados = exercicios_adequados.exclude(restricoes__icontains=lesao.strip())

    # Excluir exercícios de acordo com as observações
    observacoes = aluno.get_observacoes_list()
    for observacao in observacoes:
        exercicios_adequados = exercicios_adequados.exclude(restricoes__icontains=observacao.strip())


    # Filtrar por objetivos específicos
    objetivos = aluno.get_objetivos_list()
    for objetivo in objetivos:
        exercicios_adequados = exercicios_adequados.filter(objetivos__icontains=objetivo.strip())

    return exercicios_adequados
