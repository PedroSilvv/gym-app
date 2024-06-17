from django.db import models
from user.models import Aluno, CustomUser

RESTRICOES_CHOICES = [
    ('Cabeça', 'Cabeça'),
    ('Pescoço', 'Pescoço'),
    ('Ombro', 'Ombro'),
    ('Braço', 'Braço'),
    ('Cotovelo', 'Cotovelo'),
    ('Antebraço', 'Antebraço'),
    ('Punho', 'Punho'),
    ('Mão', 'Mão'),
    ('Coluna', 'Coluna'),
    ('Quadril', 'Quadril'),
    ('Coxa', 'Coxa'),
    ('Joelho', 'Joelho'),
    ('Perna', 'Perna'),
    ('Tornozelo', 'Tornozelo'),
    ('Pé', 'Pé'),
    ('Diabetes', 'Diabetes'),
    ('Hipertensao', 'Hipertensão'),
    ('Problemas_Cardiacos', 'Problemas cardíacos'),
    ('Asma', 'Asma'),
    ('Alergias', 'Alergias'),
    ('Intolerancia_Alimentar', 'Intolerância alimentar'),
    ('Vegetariano', 'Vegetariano'),
    ('Vegano', 'Vegano'),
]

OBJETIVOS_CHOICES = [
    ('Perda de Peso', 'Perda de Peso'),
    ('Ganho de Massa Muscular', 'Ganho de Massa Muscular'),
    ('Manutenção de Peso', 'Manutenção de Peso'),
    ('Melhora da Resistência', 'Melhora da Resistência'),
    ('Melhora da Flexibilidade', 'Melhora da Flexibilidade'),
    ('Melhora da Saúde Cardiovascular', 'Melhora da Saúde Cardiovascular'),
    ('Reabilitação', 'Reabilitação'),
    ('Preparação para Competição', 'Preparação para Competição'),
    ('Redução do Estresse', 'Redução do Estresse'),
    ('Aumento da Energia', 'Aumento da Energia'),
    ('Melhora da Postura', 'Melhora da Postura'),
    ('Condicionamento Geral', 'Condicionamento Geral'),
    ('Aprimoramento de Habilidades Específicas', 'Aprimoramento de Habilidades Específicas'),
    ('Saúde Mental', 'Saúde Mental'),
]


class Exercicio(models.Model):

    NIVEL_CHOICES = [
        ('Iniciante', 'iniciante'),
        ('Intermediario', 'intermediario'),
        ('Avançado', 'avançado')
    ]

    TIPO_CHOICES = [
        ('Cardiovascular', 'Cardiovascular'),
        ('Definição', 'Definição'),
        ('Força', 'Força'),
        ('Funcional', 'Funcional'),
        ('Hipertrofia', 'Hipertrofia'),
        ('Resistencia', 'Resistencia'),
        ('Terapeutico', 'Terapeutico'),
    ]
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    #ENUM FIELDS
    tipo = models.CharField(max_length=25, choices=TIPO_CHOICES)  
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)

    #LIST FIELDS  
    objetivos = models.CharField(max_length=200, blank=True, null=True)
    restricoes = models.TextField(null=True)

    
    def __str__(self):
        return self.nome

    def get_restricoes_list(self):
        if self.restricoes:
            return self.restricoes.split(',')
        return []
    
    def set_restricoes_list(self, restricoes_list):
        self.restricoes = ','.join(restricoes_list)

    def get_objetivos_list(self):
        if self.objetivos:
            return self.objetivos.split(',')
        return []

    def set_objetivos(self, objetivos_list):
        self.objetivos = ','.join(objetivos_list)
        



class Treino(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    personal = models.ForeignKey(CustomUser,null=True ,on_delete=models.CASCADE)
    data = models.DateField()
    concluido = models.BooleanField(default=False)
    aceitou = models.BooleanField(default=False, null=True)

    def __str__(self):
        return f"Treino de {self.aluno.user.nome} em {self.data}"

    @property
    def series(self):
        return self.serie_set.all()
    


class Serie(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    numero_series = models.PositiveIntegerField()
    repeticoes_por_serie = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.exercicio.nome} - (Treino: {self.treino.aluno.user.nome} em {self.treino.data})"
    



