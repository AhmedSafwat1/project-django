from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from projects.models import *
from django.contrib import messages
from django.contrib.auth import logout


# Create your views here.
from users.forms import *
from django.contrib.auth import authenticate

def index(request):
    return HttpResponse("sucess")


def profile(request, uid):
    user = get_object_or_404(User, id=uid)
    categories = Categories.objects.all()
    flag = 1
    context = {
        "userprofile": user,
        "userProject": user.projects_set.all(),
        "categories": categories,
        "flag": flag,
        "pcount": user.projects_set.count(),
        "suppliers": user.supplier_set.all(),
        "scount": user.supplier_set.count()
    }
    return render(request, "users/profile.html", context)


def deleteAccount(request):
    user = User.objects.get(id=2)
    form = UserFormPassword(request.POST)
    if form.is_valid():
        print("wwww")
        user = authenticate(username=user.username, password=form.cleaned_data.get("password"))
        if user is not None:
            user.delete()
            messages.success(request, "Delete Account Sucess")
            return redirect("/projects/home")
        else:
            messages.error(request, "Enter Valid password ")
    messages.error(request, form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def logout_view(request):
    logout(request)
    return redirect("/projects/home")
