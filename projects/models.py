from django.db import models
import uuid

from django.db.models.deletion import CASCADE
from users.models import Profile
# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(
        null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title
    class Meta:
        #Ordem
        #created = os mais antigos(Ascendente)
        #-created = os mais recentes(Descrescente)
        ordering = ['-vote_ratio', '-vote_total', 'title']
        
    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = '/images/default.jpg'

        return url   
        
    @property 
    def reviewers(self):#lista completa de quem deu review no projeto
           query_set=self.review_set.all().values_list('owner__id', flat=True)
           
        
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()#Pega todas as reviews da DB
        upVotes = reviews.filter(value='up').count()
        totalVotes= reviews.count() #Conta a quantidade de votos
        
        ratio = (upVotes /totalVotes) * 100 #Calcula o ratio
        #Atualiza a DB
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()
    
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    #Liga owner e project para evitar que uma pessoa faça inumeros reviews de um unico projeto
    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name
