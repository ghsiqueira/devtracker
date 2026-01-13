import logging
from datetime import timedelta
from django.utils import timezone
from django.db.models import Max 
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task
from .forms import TaskForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
import google.generativeai as genai
from django.conf import settings
import json

logger = logging.getLogger(__name__)

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    search_query = request.GET.get('q', '')
    if search_query:
        projects = projects.filter(title__icontains=search_query)
    return render(request, 'project_list.html', {'projects': projects, 'search_query': search_query})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_list')
    else:
        form = ProjectForm()
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    tasks = project.tasks.all()
    
    filter_status = request.GET.get('filter')
    today = timezone.now().date()
    
    if filter_status == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif filter_status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif filter_status == 'high':
        tasks = tasks.filter(priority='H')
    elif filter_status == 'overdue': 
        tasks = tasks.filter(is_completed=False, due_date__lt=today)

    sort_by = request.GET.get('sort', '-id') 
    
    if sort_by == 'due_date':
        tasks = tasks.order_by('due_date') 
    elif sort_by == 'priority':
        tasks = tasks.order_by('priority', 'due_date') 
    else:
        tasks = tasks.order_by(sort_by)

    return render(request, 'project_detail.html', {
        'project': project, 
        'tasks': tasks,
        'filter': filter_status,
        'sort': sort_by
    })

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', id=project.id)
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form, 'project': project})

@login_required
def task_complete(request, id):
    task = get_object_or_404(Task, id=id, project__user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('project_detail', id=task.project.id)

@login_required
def project_update(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

@login_required
def project_delete(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    if request.method == 'POST':
        project.delete()
        return redirect('project_list')
    return render(request, 'confirm_delete.html', {'object': project, 'type': 'Project'})

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, project__user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', id=task.project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form, 'project': task.project})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, project__user=request.user)
    project_id = task.project.id
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', id=project_id)
    return render(request, 'confirm_delete.html', {'object': task, 'type': 'Task'})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def ai_generate_tasks(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    
    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        
        model = genai.GenerativeModel(
            'gemini-flash-latest',
            generation_config={"response_mime_type": "application/json"}
        )
        
        prompt = f"""
            Atue como um Tech Lead Sênior rigoroso.
            PROJETO: "{project.title}"
            DESCRIÇÃO: "{project.description}"

            MISSÃO:
            Crie um Backlog (WBS) técnico e sequencial.

            REGRAS DE QUANTIDADE (AUTO-ADAPTÁVEL):
            - Projetos Simples: 10-15 tarefas.
            - Projetos Complexos: 30-40 tarefas.

            REGRAS DE PRIORIDADE (RIGOROSAS):
            A IA costuma marcar tudo como 'High'. NÃO FAÇA ISSO.
            Siga esta distribuição estrita:
            - H (High): Max 20% (Apenas infraestrutura crítica e blockers iniciais).
            - M (Medium): 60% (A grande massa do desenvolvimento funcional).
            - L (Low): 20% (Melhorias, UI polishes, testes não-críticos).

            REGRAS DE PRAZO:
            Estime "days_from_start" sequencialmente para criar um cronograma realista.
            
            FORMATO JSON:
            [
                {{"title": "Configurar Repo e CI/CD", "priority": "H", "days_from_start": 1}},
                {{"title": "Criar tela de Login", "priority": "M", "days_from_start": 3}}
            ]
        """
        
        response = model.generate_content(prompt)
        tasks_data = json.loads(response.text)
        
        if not isinstance(tasks_data, list):
            raise ValueError("Resposta IA inválida")
        
        last_task_date = Task.objects.filter(project__user=request.user).aggregate(Max('due_date'))['due_date__max']
        today = timezone.now().date()
        
        if last_task_date and last_task_date >= today:
            start_date = last_task_date + timedelta(days=1)
        else:
            start_date = today

        created_count = 0
        for task_item in tasks_data:
            if 'title' in task_item:
                days_offset = task_item.get('days_from_start', 1)
                final_date = start_date + timedelta(days=days_offset)
                
                Task.objects.create(
                    project=project,
                    title=task_item['title'],
                    priority=task_item.get('priority', 'M'),
                    due_date=final_date
                )
                created_count += 1
        
        messages.success(request, f"🚀 {created_count} tarefas geradas (Prioridades Recalibradas)!")
        
    except Exception as e:
        logger.error(f"AI Error: {e}")
        messages.error(request, "A IA teve um problema técnico. Tente novamente.")
    
    return redirect('project_detail', id=project_id)