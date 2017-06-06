from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.decorators import method_decorator

from django.views.generic import DeleteView, ListView

import hashlib
import random

from clients.forms import RegisterForm, ClientRegisterForm
from clients.models import Client


def activate(request, id, token):
    """
    User activation
    """

    try:
        user = User.objects.get(pk=id)
    except:
        user = None

    if user is not None:
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')


@login_required(login_url='/login/')
def create_client(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            client = form.save(commit=False)
            client.creator_id = request.user.pk
            client.save()
            return redirect('/')
    else:
        form = ClientRegisterForm()
    return render(request, 'clients/createClient.html', {'form': form})


def index(request):
    return render(request, 'clients/index.html')


class InfoClients(ListView):
    model = Client
    template_name = "clients/info_clients.html"

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(InfoClients, self).dispatch(request, *args, **kwargs)


def client_details(request, pk):
    client = get_object_or_404(Client, pk=pk)
    form = RegisterForm()
    return render(request, 'clients/client_details.html', {'form': form, 'client': client})


def register(request):
    """
    registration of user with sending message and confirmation on mail
    """

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            salt = str(random.random()).encode('utf-8')
            token = hashlib.md5(salt + str(user.email).encode('utf-8')).hexdigest()
            message = render_to_string('clients/activation_email.html', {
                'id': user.pk,
                'user': user,
                'domain': current_site.domain,
                'token': token,
            })
            send_mail('Activate Your account', message, 'company@company.com', [user.email], fail_silently=False)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'clients/register.html', {'form': form})
