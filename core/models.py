from django.db import models
from django.contrib.auth.models import User

class Projeto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    @property
    def progresso(self):
        total_tarefas = self.tarefas.count()
        if total_tarefas == 0:
            return 0
        concluidas = self.tarefas.filter(concluida=True).count()
        return int((concluidas / total_tarefas) * 100)

class Tarefa(models.Model):
    projeto = models.ForeignKey(Projeto, related_name='tarefas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    concluida = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo