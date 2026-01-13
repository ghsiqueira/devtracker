from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Project, Task
from .forms import TaskForm, ProjectForm

@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'project_detail.html', {'project': project})

@login_required
def task_create(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
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
    task = get_object_or_404(Task, id=id)
    task.is_completed = not task.is_completed 
    task.save()
    return redirect('project_detail', id=task.project.id)

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