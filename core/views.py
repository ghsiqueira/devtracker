from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task
from .forms import TaskForm

def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    return render(request, 'project_detail.html', {'project': project})

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

def task_complete(request, id):
    task = get_object_or_404(Task, id=id)
    task.is_completed = not task.is_completed 
    task.save()
    return redirect('project_detail', id=task.project.id)