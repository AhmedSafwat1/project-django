from django.forms import ModelForm
from .models import *
class ProjectFormAdd(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'details',
                  'categorie', 'totalTarget',
                  'startCampaign', 'endcampaign',
                  'user']


class ProjectFormAddImage(ModelForm):
    class Meta:
        model = ImageProject
        fields = ['project', 'image']
