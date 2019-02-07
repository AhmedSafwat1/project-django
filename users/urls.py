from django.urls import path
from .views import *
app_name = "users"
urlpatterns = [
   path("profile/<int:uid>", profile, name="profile"),
   path("delete", deleteAccount, name="delete"),
   path("edit/<int:uid>", editprofile, name="edit"),
   path("logout", logout_view , name="logout"),
   path("login", loginuser, name="login2"),
   path("register", register2 ,name="register"),

]
