# Generated by Django 4.1.7 on 2024-05-22 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('Cardiovascular', 'Cardiovascular'), ('Definição', 'Definição'), ('Força', 'Força'), ('Funcional', 'Funcional'), ('Hipertrofia', 'Hipertrofia'), ('Resistencia', 'Resistencia'), ('Terapeutico', 'Terapeutico')], max_length=25)),
                ('nivel', models.CharField(choices=[('Iniciante', 'iniciante'), ('Intermediario', 'intermediario'), ('Avançado', 'avançado')], max_length=20)),
                ('objetivos', models.CharField(blank=True, max_length=200, null=True)),
                ('restricoes', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Treino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('concluido', models.BooleanField(default=False)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_series', models.PositiveIntegerField()),
                ('repeticoes_por_serie', models.PositiveIntegerField()),
                ('exercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treino.exercicio')),
                ('treino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='treino.treino')),
            ],
        ),
    ]
