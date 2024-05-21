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
    esportes_praticados = models.ManyToManyField(Esporte, related_name='usuarios')
    lesoes = models.TextField(blank=True, null=True)
    objetivos = models.TextField(max_length=200, blank=True, null=True)
    peso = models.FloatField(blank=True, null=True)
    altura = models.PositiveIntegerField(blank=True, null=True)
    experiencia = models.CharField(max_length=100, blank=True, null=True, choices=EXP_CHOICES)  # iniciante, intermediário, avançado
    dias_treino_semanal = models.IntegerField(null=True)


    def __str__(self):
        return self.user.username
    
    def get_lesoes_list(self):
        if self.lesoes:
            return self.lesoes.split(',')
        return []

    def set_lesoes(self, lesoes_list):
        self.lesoes = ','.join(lesoes_list)
    
    