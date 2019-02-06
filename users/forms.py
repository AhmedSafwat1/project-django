from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
class UserFormEdit(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class profileFormEdit(ModelForm):
    class Meta:
        model = Profile
        fields = ('facebook', 'country', 'birth_date','phone','image')


class UserFormPassword(ModelForm):
    class Meta:
        model = User
        fields = ('password',)