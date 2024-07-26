from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review


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
#@permission_classes([IsAuthenticated])
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



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    #Valor repassado no BODY da pagina
    data = request.data 
    #get_or_create vai verificar se existe ou nao o review e se nao existir, vai criar
    review, created = Review.objects.get_or_create(
        owner = user,
        project= project,
    )
    
    review.value = data['value']
    review.save()
    project.getVoteCount
    
    serializer = ProjectSerializer(project, many=False)
    
    return Response(serializer.data)