from django.urls import path
from .views import *
app_name = "projects"
urlpatterns = [
    path('', index),
    path('add',add, name="add"),
    path('new',new,name="new"),
    path("home", index, name="home"),
    path("donate/<int:pid>", donate, name="donate"),
    path("categorie/<int:cid>", view, name="show"),
    path("search", search, name="search"),
    path("details/<int:pid>", details, name="detail"),
    path("rate/<int:pid>", rateing, name="rate"),
    path("report/<int:pid>/<int:cid>", reportComment, name="reportcomment"),
    path("report/<int:pid>", reportProject, name="reportproject")
]
