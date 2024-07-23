from django.db.models import Q
from .models import Profile, Skill


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