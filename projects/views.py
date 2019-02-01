from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from django.http import QueryDict
from .models import *

# Create your views here.
def dict_querydict(dict_):
   """
   Converts a value created by querydict_dict back into a Django QueryDict value.
   """
   q = QueryDict("", mutable=True)
   for k, v in dict_.items():
      q.setlist(k, v)
   q._mutable = False
   return q
def index(request):
   f = ProjectFormAdd()
   return render(request,"projects/tetting.html",{"f":f})

def add(request):
   f = ProjectFormAdd(request.POST)
   f.save()
   p = Projects.objects.latest('id')
   for img in request.FILES.getlist("image"):
      image = ImageProject()
      image.image = img
      image.project = p
      image.save()
   return HttpResponse(f)
