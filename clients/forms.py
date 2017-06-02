from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'email',)


class Profile(models.Model):
    user = models.OneToOneField(User)
