from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginationProjects(request, projects, results):
    #Paginacao dos projetos
    #page = 1 #Pagina
    page = request.GET.get('page')
    # results = 2 #Quantidade de Projetos por pagina
    paginator = Paginator(projects, results)
    #Tente pegar a pagina
    try:
        projects = paginator.page(page)
    #Se o erro for PageNotAnInteger, atribui pagina = 1    
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    #Se o erro for EmptyPage, atribui pagina = numero_paginas (Ultima Pagina)    
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page) 
        
    return projects, paginator

def searchProjects(request):
    search_query = ''
    
    #Pega o valor no campo search_query do html
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    tags = Tag.objects.filter(name__icontains=search_query)
        
    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)|
        Q(description__icontains=search_query)|
        Q(tags__in=tags)|
        Q(owner__name__icontains=search_query))
    
    return projects, search_query