from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from .forms import ProjectForm

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
            return redirect('projects')
        
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
    return render(request, 'projects/delete_template.html', context)