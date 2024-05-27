import random

from treino.models import Exercicio, RESTRICOES_CHOICES, OBJETIVOS_CHOICES

# Define a lista de tipos e níveis
TIPO_CHOICES = ['Cardiovascular', 'Definição', 'Força', 'Funcional', 'Hipertrofia', 'Resistencia', 'Terapeutico']
NIVEL_CHOICES = ['Iniciante', 'Intermediario', 'Avançado']

# Converte os choices em listas de strings
restricoes_options = [choice[0] for choice in RESTRICOES_CHOICES]
objetivos_options = [choice[0] for choice in OBJETIVOS_CHOICES]

# Função para criar um exercício
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

# Função para gerar combinações aleatórias de objetivos e restrições
def generate_combinations(options, max_length):
    num_options = random.randint(1, max_length)
    selected_options = random.sample(options, num_options)
    return ','.join(selected_options)

# Criação de 40 exercícios
for i in range(1, 41):
    nome = f"Exercicio {i}"
    descricao = f"Descricao do exercicio {i}"
    tipo = random.choice(TIPO_CHOICES)
    nivel = random.choice(NIVEL_CHOICES)
    objetivos = generate_combinations(objetivos_options, 5)
    restricoes = generate_combinations(restricoes_options, 5)
    
    criar_exercicio(nome, descricao, tipo, nivel, objetivos, restricoes)

print("40 exercícios foram criados com sucesso!")
