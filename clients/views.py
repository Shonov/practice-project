from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail

import hashlib
import random

from clients.forms import RegisterForm


def index(request):
    return render(request, 'clients/index.html')


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


def create_client(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'clients/register.html', {'form': form})



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
