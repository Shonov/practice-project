import datetime
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget

from clients.models import Client,Comment


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email')


class Profile(models.Model):
    user = models.OneToOneField(User)


class ClientRegisterForm(ModelForm):
    class Meta:
        model = Client
        fields = ('photo', 'name', 'surname', 'birth_Day')

        year = datetime.date.today().year

        widgets = {
            'birth_Day': SelectDateWidget(years=range(year, year - 100, -1))
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text', 'time')