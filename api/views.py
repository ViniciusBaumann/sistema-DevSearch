from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project


@api_view(['GET'])
def getRoutes(request):
    
    routes = [
        {'GET':'/api/projects'},
        {'GET':'/api/projects/id'},
        {'POST':'/api/projects/id/vote'},
        
        {'POST':'/api/user/token'},
        {'POST':'/api/user/token/refresh'},
    ]
        
    return Response(routes)
##Mostra todos os projetos com o ID serializado
@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    
    return Response(serializer.data)

##Mostra apenas um projeto com o id do projeto sendo PK
@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    #lembrar de many=false quando for apenas uma objeto
    serializer = ProjectSerializer(projects, many=False)
    
    return Response(serializer.data)