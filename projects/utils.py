from django.db.models import Q
from .models import Project, Tag


def searchProject(request):
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