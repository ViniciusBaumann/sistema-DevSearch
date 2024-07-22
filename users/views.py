from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm

# Create your views here.

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
            return redirect('login')   

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {"login": login}
    return render(request, 'users/login_register.html', context)

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #Salvar username como lowercase
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')

            login(request, user)
            return redirect('account')
        
        else:
            messages.error(request, 'Error during the registration')

    context= {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User is logged out')
    return redirect('login')


def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')#Visivel apenas para logados e se nao estiver logado sera redirecionado para 'login'
def userAccount(request):
    profile = request.user.profile # request.user = Pergutando ao servidor qual usuario esta logado e pegando as infos (Profile)
    
    skills = profile.skill_set.all()#Pega todas as skills do usuario do DB
    projects = profile.project_set.all()#Pega todas os projetos do usuario do DB

    context = {'profile':profile, 'skills':skills, 'projects':projects}#envia as infos do perfil ao account.html para ser usado

    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editAccount(request):
    #pergunta ao server qual eh o USUARIO logado e seu perfil
    profile = request.user.profile
    #Sinal que da o update no USUARIO do sistema e AutoPreencimento dos campos ja preenchidos no sistema
    form = ProfileForm(instance=profile)
    #Recebe o formulado de profile_form.html com enctype
    if request.method == "POST":
        #INSTANCE = QUAL O PERFIL QUE SERA ALTERADO
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid:
            form.save()
            
            messages.success(request, 'User account was edited')
            
            return redirect('account')
        
    context = {'form':form}
    return render(request, 'users/profile_form.html', context)
    