from django.contrib import admin
from django.urls import path, include
from core.views import (project_list, project_detail, project_create, project_update, project_delete, task_create, task_complete, task_update, task_delete, signup, ai_generate_tasks)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', project_list, name='project_list'),
    path('signup/', signup, name='signup'),
    path('project/add/', project_create, name='project_create'),
    path('project/<int:id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/task/add/', task_create, name='task_create'),
    path('task/<int:id>/complete/', task_complete, name='task_complete'),
    path('project/<int:id>/edit/', project_update, name='project_update'),
    path('project/<int:id>/delete/', project_delete, name='project_delete'),
    path('task/<int:id>/edit/', task_update, name='task_update'),
    path('task/<int:id>/delete/', task_delete, name='task_delete'),
    path('project/<int:project_id>/ai-generate/', ai_generate_tasks, name='ai_generate_tasks'),
]