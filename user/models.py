from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, Group, Permission
from django.core.exceptions import ValidationError

LESOES_CHOICES = [
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
    ('Pé', 'Pé')
]

OBSERVACOES_CHOICES = [
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


class Esporte(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.nome

class CustomUser(AbstractUser):


    nome = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=11, null=True)
    cpf = models.CharField(max_length=11, null=True)
    endereco = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.username

    groups = models.ManyToManyField(
    Group,
    related_name='customuser_set',
    blank=True,
    help_text=(
        'The groups this user belongs to. A user will get all permissions '
        'granted to each of their groups.'
    ),
    related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
    Permission,
    related_name='customuser_set',
    blank=True,
    help_text='Specific permissions for this user.',
    related_query_name='customuser',
    )


class Aluno(models.Model):


    EXP_CHOICES = [
        ('Iniciante', 'iniciante'),
        ('Intermediario', 'intermediario'),
        ('Avançado', 'avançado')
    ]


    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    peso = models.FloatField(blank=True, null=True)
    altura = models.PositiveIntegerField(blank=True, null=True)
    experiencia = models.CharField(max_length=100, blank=True, null=True, choices=EXP_CHOICES) 
    dias_treino_semanal = models.IntegerField(null=True)

    #LIST FIELDS
    observacoes = models.TextField(blank=True, null=True)
    objetivos = models.TextField(max_length=200, blank=True, null=True)
    lesoes = models.TextField(blank=True, null=True)
    esportes_praticados = models.ManyToManyField(Esporte, related_name='usuarios')


    def __str__(self):
        return f"Nome: {self.user.nome} - Username: {self.user.username}"

    def get_lesoes_list(self):
        if self.lesoes:
            return self.lesoes.split(',')
        return []

    def set_lesoes(self, lesoes_list):
        self.lesoes = ','.join(lesoes_list)

    
    def get_observacoes_list(self):
        if self.observacoes:
            return self.observacoes.split(',')
        return []
    
    def set_observacoes(self, observacoes_list):
        self.observacoes = ','.join(observacoes_list)

    
    def get_objetivos_list(self):
        if self.objetivos:
            return self.objetivos.split(',')
        return []

    def set_objetivos(self, objetivos_list):
        self.objetivos = ','.join(objetivos_list)