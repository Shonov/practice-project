from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.utils import six
from django.urls import reverse
from django.contrib.auth.models import User
from django.shortcuts import render
from .filters import UserFilter

from django.views.generic import DeleteView, ListView, DetailView, UpdateView

import hashlib
import random

from clients.forms import RegisterForm, ClientRegisterForm
from clients.models import Client


class ClientsListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/clients_list_view.html"
    ordering = 'name'

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ClientsListView, self).dispatch(request, *args, **kwargs)

    def get_ordering(self):
        self.ordering = self.request.GET.get('order', 'field')
        order = self.request.GET.get('order', 'name')
        if self.ordering == 'field':
            order = "-" + order
        return order

    def get_context_data(self, *args, **kwargs):
        context = super(ClientsListView, self).get_context_data(*args, **kwargs)
        context['order'] = self.ordering
        return context

    # def search(self):
    #     if self.request.method == 'POST':
    #         return Client.objects.filter(self.request.POST['search'])


class ClientDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = Client
    context_object_name = 'client'
    template_name = 'clients/client_details.html'

    def get_object(self):
        object = super(ClientDetailView, self).get_object()
        if not self.request.user.is_authenticated():
            raise Http404
        return object


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'clients/client_details.html'

    def get_success_url(self):
        return '/info_clients/'

    def get_object(self):
        obj = super(ClientDeleteView, self).get_object()
        if not obj.creator_id == self.request.user.id:
            raise Http404
        return obj


class ClientUpdateView(UpdateView):
    form_class = ClientRegisterForm
    model = Client
    template_name = 'clients/update_client.html'
    success_url = '/info_clients/'


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


class DeleteClient(DeleteView):
    model = Client
    template_name = 'clients/client_details.html'
    success_url = '/info_clients/'

    def get_object(self):
        obj = super(DeleteClient, self).get_object()
        if not obj.creator_id == self.request.user.id:
            return obj
class Search():
    def search(request):
        user_list = User.objects.all()
        user_filter = UserFilter(request.GET, queryset=user_list)
        return render(request, 'search/user_list.html', {'filter': user_filter})