from django.contrib import admin
from .models import Projeto, Tarefa

class TarefaInline(admin.TabularInline):
    model = Tarefa
    extra = 1

class ProjetoAdmin(admin.ModelAdmin):
    inlines = [TarefaInline]

admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Tarefa)