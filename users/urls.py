from django.urls import path
from .views import *
app_name = "users"
urlpatterns = [
   path("", index),
   path("profile/<int:uid>", profile, name="profile"),
   path("delete", deleteAccount, name="delete"),
]
