from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from clients.models import Client


def index(request):
    client = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': client})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "clients/register.html", {
        'form': form,
    })

def login(request):
    username = request.POST['login']
    password = request.POST['password']
    user = auth.authenticate(login=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/login.html")
    else:
        return HttpResponseRedirect()

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")