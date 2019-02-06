from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from django.http import QueryDict
from .models import *
from django.forms import formset_factory
from django.forms import modelformset_factory
from django.db.models import Avg
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404,redirect
from django.contrib import messages

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
    return render(request, "projects/tetting.html", {"f": f})


def add(request):
    f = ProjectFormAdd(request.POST)
    print(request.POST);
    test = {
        'title': ['testfrom ppp'],
        'details': ['wewf'],
        'categorie': ['2'],
        'user': ['1'],
        'totalTarget': ['1400'],
        'startCampaign': ['2019-02-05'],
        'endcampaign': ['2019-02-13']
    }
    test = dict_querydict(test)
    f = ProjectFormAdd(test)
    print(request.FILES)
    print(request.FILES['image'])
    count = len(request.FILES.getlist("image"))
    ImageFormSet = modelformset_factory(ImageProject,
                                        form=ImageForm, extra=5)
    formset = ImageFormSet(request.POST, request.FILES)
    test2 = {
        "project": ['43'],
        "form-MAX_NUM_FORMS": [formset.management_form]
    }
    test2 = dict_querydict(test2)
    f2 = ProjectFormAddImage(test2, request.FILES);

    # print(formset);
    p = Projects.objects.get(id=43)
    for form in formset:
        print(form.as_table())
        # if form:
        #    image = form['image']
        #    Post = ImageProject(project=p, image=image)
        #    Post.save()

    f2 = ProjectFormAddImage(test2)
    # f2.save()
    # ====================================

    # =================================
    # f.save()
    # f.save()
    # p = Projects.objects.latest('id')
    # for img in request.FILES.getlist("image"):
    #    image = ImageProject()
    #    image.image = img
    #    image.project = p
    #    image.save()

    # p.first().rate_set.all().aggregate(Avg('rate')) to get avg
    print(formset.management_form)
    return HttpResponse(f)


# start project
def checkUNique(tag):
    if ProjectTage.objects.filter(tage=tag).exists():
        return ProjectTage.objects.get(tage=tag)
    else:
        t = ProjectTage(tage=tag)
        t.save()
        return t


def new(request):
    context = {
        "categories": Categories.objects.all(),
    }
    if request.POST:
        newProject = ProjectFormAdd(request.POST, request.FILES)
        if newProject.is_valid():
            newProject.save()
            print(request.FILES)
            p = Projects.objects.latest('id')
            if request.POST['tags']:
                tags = request.POST['tags'].split(",")
                # print(tags);
                for i in tags:
                    p.tags.add(checkUNique(i))
                    # 'image/png'
                for img in request.FILES.getlist("image"):
                    image = ImageProject()
                    image.image = img
                    print(img.__dict__)
                    image.project = p
                    image.save()
            messages.success(request, "Add new Project Sucess")
            return redirect("/projects")
        else:
            context['form'] = newProject
            context['data'] = request.POST
            print(newProject.errors.items);
    return render(request, "projects/FormProject.html", context)


# home view

def index(request):
    projects = Projects.objects.all()
    ProjectRate = Projects.objects.annotate(avg=Avg("rate__rate")).order_by('-avg')[:5]
    lastProject = Projects.objects.order_by('-id')[:5]
    featureProjects = FeatureProjects.objects.all()
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "ProjectRate": ProjectRate,
        "lastProject": lastProject,
        "featureProjects":featureProjects,
        "categories":categories
    }
    return render(request, "projects/projectHome.html", context)

def view(request,cid):
    projects = get_object_or_404(Categories, id=cid)
    categories = Categories.objects.all()
    context = {
        "projects":projects.projects,
        "categories": categories,
        "categieNmae": projects.name
    }

    return  render(request,"projects/view.html",context)

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        mode = form.cleaned_data.get("mode")
        searching = form.cleaned_data.get("search")
        if mode == "1":
            projects = ProjectTage.objects.filter(tage=searching)
            if projects:
                projects = projects[0].project_all()
        else:
            projects = Projects.objects.filter(title=searching)
    categories = Categories.objects.all()
    context = {
        "projects": projects,
        "categories": categories,
        "categieNmae": searching
    }
    return  render(request,"projects/view.html",context)

def donate(request,pid):
    project  = get_object_or_404(Projects,id=pid)
    form = SupllierForm(request.POST)
    if form.is_valid():
        user = get_object_or_404(User,id=1)
        new_s = Supplier(project=project,supplierName=user,quanty=request.POST['quanty'])
        new_s.save();
        messages.success(request,"Donate Sucess")
        return  HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        messages.error(request, "Error not Donate sucess")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def details(request, pid):
    categories = Categories.objects.all()
    project = get_object_or_404(Projects, id=pid)

    context = {
        "categories": categories,
        "images":project.allImage(),
        "project":project,
        "commentcount": project.comments().count()
    }
    return  render(request, "projects/details.html", context )

def rateing(request, pid):
    user1 = User.objects.get(id=1)
    project1 = get_object_or_404(Projects,id=pid);
    r =request.POST['rate']
    if(Rate.objects.filter(project=project1, user=user1)):
        Rate.objects.filter(project=project1, user=user1).update(rate=r)
        messages.success(request, "Rateing Sucess")
    else:
        Rate.objects.create(project=project1, user=user1, rate=r)
        messages.success(request, "Rateing Sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def reportProject(request, pid):
    form = ReportForm(request.POST)
    if form.is_valid():
        project= get_object_or_404(Projects,id=pid)
        user = get_object_or_404(User ,id=1)
        content = form.cleaned_data.get("content")
        ReportProject.objects.create(project=project,user=user,content=content)
        messages.success(request, "Reporting Sucess")
    else:
        messages.error(request, "Error not Report sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def reportComment(request, pid, cid):
    form = ReportForm(request.POST)
    if form.is_valid():
        project= get_object_or_404(Projects,id=pid)
        comment = get_object_or_404(Comment,id=cid)
        user = get_object_or_404(User ,id=1)
        content = form.cleaned_data.get("content")
        ReportComment.objects.create(comment=comment,user=user,content=content)
        messages.success(request, "Reporting Sucess")
    else:
        messages.error(request, "Error not Report sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def comment(request, pid):
    form = CommentForm(request.POST)

    if form.is_valid():
        project = get_object_or_404(Projects, id=pid)
        user = get_object_or_404(User, id=1)
        content = form.cleaned_data.get("content")
        Comment.objects.create(user=user, project=project, content=content)
        messages.success(request, "commented Sucess")
    else:
        messages.error(request, "Error not comment sucess sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def deletProject(request, cid):
    user = User.objects.get(id=1)
    project = get_object_or_404(Projects,id=cid, user=user)
    project.delete()
    messages.success(request, "Delete Sucess")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



