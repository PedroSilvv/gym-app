from ..models import Exercicio, Treino, Serie
from user.models import Aluno
from datetime import date

def filtrar_exercicios(aluno):
    # Filtrar por exp do Aluno
    exercicios_adequados = Exercicio.objects.filter(nivel__iexact=aluno.experiencia)

    # Excluir exercícios de acordo com as lesões
    lesoes = aluno.get_lesoes_list()
    for lesao in lesoes:
        exercicios_adequados = exercicios_adequados.exclude(restricoes__icontains=lesao.strip())

    # Excluir exercícios de acordo com as observações
    observacoes = aluno.get_observacoes_list()
    for observacao in observacoes:
        exercicios_adequados = exercicios_adequados.exclude(restricoes__icontains=observacao.strip())

    # Filtrar por objetivos específicos
    # objetivos = aluno.get_objetivos_list()
    # print(objetivos)
    # for objetivo in objetivos:
    #     if exercicios_adequados.filter(objetivos__icontains=objetivo.strip()).exists():
    #         exercicios_adequados = exercicios_adequados.filter(objetivos__icontains=objetivo.strip())
    # print(exercicios_adequados)
    return exercicios_adequados

def determinar_series_repeticoes(experiencia, tipo_exercicio):
    if experiencia == 'Iniciante':
        if tipo_exercicio in ['Força', 'Hipertrofia']:
            return 2, 12
        else:
            return 3, 15
    elif experiencia == 'Intermediario':
        if tipo_exercicio in ['Força', 'Hipertrofia']:
            return 3, 10
        else:
            return 4, 12
    else:  # avançado
        if tipo_exercicio in ['Força', 'Hipertrofia']:
            return 4, 8
        else:
            return 5, 10


def gerar_treino_para_aluno(aluno):
    exercicios_adequados = filtrar_exercicios(aluno)

    if not exercicios_adequados.exists():
        raise ValueError("Nenhum exercício adequado disponível para gerar treino")

    treino = Treino.objects.create(aluno=aluno, data=date.today())

    # Tipos de exercícios a incluir no treino
    tipos_exercicios = ['Cardiovascular', 'Definição', 'Força', 'Funcional', 'Hipertrofia', 'Resistencia', 'Terapeutico']
    #ex_por_treino = 5 if aluno.experiencia == "Iniciante" else ( 6 if aluno.experiencia == "Intermediario" else )

    for tipo in tipos_exercicios:
        # Selecionar os exercícios mais adequados para cada tipo
        exercicios_por_tipo = exercicios_adequados.filter(tipo=tipo)
        
        if exercicios_por_tipo.exists():
            # Escolher o exercício com a menor quantidade de restrições ou que atenda mais objetivos
            melhor_exercicio = min(
                exercicios_por_tipo,
                key=lambda e: len(e.get_restricoes_list()) / len(e.get_objetivos_list())
            )

            # Determinar o número de séries e repetições com base na experiência do aluno e no tipo de exercício
            numero_series, repeticoes_por_serie = determinar_series_repeticoes(aluno.experiencia, tipo)
            
            Serie.objects.create(
                treino=treino,
                exercicio=melhor_exercicio,
                numero_series=numero_series,
                repeticoes_por_serie=repeticoes_por_serie
            )

    return treino
