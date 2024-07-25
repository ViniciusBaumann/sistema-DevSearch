from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .utils import paginationProjects, searchProjects
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm

def projects(request):
    projects , search_query = searchProjects(request)
    projects, paginator =  paginationProjects(request, projects, 2)
    
    context = {'projects' : projects, 'search_query':search_query, 'paginator': paginator}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)#Cria uma instacia do projeto mas nao envia para a DB
            review.project = projectObj
            review.owner = request.user.profile #Vincula o dono do projeto ao peril logado atualmente
            review.save()
            
            projectObj.getVoteCount#Usa sem o () mesmo
            
            messages.success(request, "Review Sent!")
            return redirect('project', pk=projectObj.id)
    
    return render(request, 'projects/single-project.html', {'projectObj': projectObj, 'form': form})

#impede um usuario nao autenticado de CRUD um projeto
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile #pergunta ao server qual eh o USUARIO logado e seu perfil
    form = ProjectForm()
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)#Cria uma instacia do projeto mas nao envia para a DB
            project.owner = profile #Vincula o dono do projeto ao peril logado atualmente
            project.save()
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)
    
@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile 
    project = profile.project_set.get(id=pk)
    #A linha acima verifica o projeto se ele esta vinculado ao perfil logado atualmente
    #Abaixo o modo que pode gerar uma exclusao por outro perfil 
    #project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
        
    context = {'form': form}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile 
    project = profile.project_set.get(id=pk)
    #project = Project.objects.get(id=pk)
    
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    
    context = {'project': project}
    return render(request, 'delete_template.html', context)