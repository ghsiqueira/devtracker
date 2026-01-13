from django.contrib import admin
from django.urls import path
from core.views import project_list, project_detail, task_create, task_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_list, name='project_list'),
    path('project/<int:id>/', project_detail, name='project_detail'),
    path('project/<int:project_id>/task/add/', task_create, name='task_create'),
    path('task/<int:id>/complete/', task_complete, name='task_complete'),
]