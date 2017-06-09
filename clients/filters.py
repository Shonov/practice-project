from django.contrib.auth.models import User
import django_filters

from clients.models import Client

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Client
        fields = ['name', 'surname', 'birth_Day']
