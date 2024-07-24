from django.db.models import Q
from .models import Profile, Skill

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginationProfiles(request, profiles, results):
    #Paginacao dos projetos
    #page = 1 #Pagina
    page = request.GET.get('page')
    # results = 2 #Quantidade de Projetos por pagina
    paginator = Paginator(profiles, results)
    #Tente pegar a pagina
    try:
        profiles = paginator.page(page)
    #Se o erro for PageNotAnInteger, atribui pagina = 1    
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    #Se o erro for EmptyPage, atribui pagina = numero_paginas (Ultima Pagina)    
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page) 
        
    return profiles, paginator

def searchProfiles(request):
    search_query = ''
    
    #Pega o valor no campo search_query do html
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print('SEARCH:', search_query)
    
    skills = Skill.objects.filter(name__icontains=search_query)
    #Lembrar de o valor NAME no arquivo html ser search_query    
    #Q torna a pesquisa uma QUEUE e consegue pesquisar por mais de um valor na DB
    #distinc() evita duplicatas
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query)| 
        Q(short_intro__icontains=search_query)|
        Q(skill__in=skills)
        )
    return profiles, search_query