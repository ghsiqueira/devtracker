from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task
from .forms import TaskForm, ProjectForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user)
    
    search_query = request.GET.get('q', '')
    if search_query:
        projects = projects.filter(title__icontains=search_query) 

    return render(request, 'project_list.html', {'projects': projects, 'search_query': search_query})

@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id, user=request.user)
    
    tasks = project.tasks.all().order_by('is_completed', '-id') 
    
    filter_status = request.GET.get('filter')
    if filter_status == 'pending':
        tasks = tasks.filter(is_completed=False)
    elif filter_status == 'completed':
        tasks = tasks.filter(is_completed=True)
    elif filter_status == 'high':
        tasks = tasks.filter(priority='H')

    return render(request, 'project_detail.html', {
        'project': project, 
        'tasks': tasks,     
        'filter': filter_status 
    })

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            
            leveled_up = request.user.profile.gain_xp(50)
            request.user.profile.save()
            if leveled_up:
                messages.success(request, f"🎉 LEVEL UP! You reached Level {request.user.profile.level}!")
            else:
                messages.success(request, "Project created! (+50 XP)")

            return redirect('project_list')
    else:
        form = ProjectForm()

    return render(request, 'project_form.html', {'form': form})

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

    if not task.is_completed:
        leveled_up = request.user.profile.gain_xp(10)
        if leveled_up:
            messages.success(request, f"🎉 LEVEL UP! You reached Level {request.user.profile.level}!")
    else:
        request.user.profile.gain_xp(-10) 
        
    request.user.profile.save()
    
    task.is_completed = not task.is_completed
    task.save()
    return redirect('project_detail', id=task.project.id)

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