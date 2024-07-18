from django.http import HttpResponse
from django.shortcuts import render
from .models import Project

def projects(request):
    projects = Project.objects.all()
    msg = 'Hello You!'
    number = 8
    context = {
        'message' : msg,
        'number' : number,
        'projects' : projects
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    return render(request, 'projects/single-project.html', {'projectObj': projectObj})

