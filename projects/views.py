from django.http import HttpResponse
from django.shortcuts import render
from . import projectlist

def projects(request):
    msg = 'Hello You!'
    number = 8
    context = {
        'message' : msg,
        'number' : number,
        'projects' : projectlist.projectsList
    }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = None
    for i in projectlist.projectsList:
        if i['id'] == pk:
            projectObj = i
    return render(request, 'projects/single-project.html', {'project': projectObj})

