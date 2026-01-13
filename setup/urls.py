from django.contrib import admin
from django.urls import path
from core.views import project_list, project_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', project_list, name='project_list'),
    path('project/<int:id>/', project_detail, name='project_detail'),
]