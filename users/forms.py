from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email','username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        #estilizacao de campo de formulario
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})    

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email','username', 'location', 'short_intro', 'bio', 'social_linkedin', 'social_website', 'social_twitter', 'social_youtube'] #Mostra todos os campos a serem modificados
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        #estilizacao de campo de formulario
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'}) 