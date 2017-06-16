from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.views.generic import DeleteView, ListView, DetailView, UpdateView
from openpyxl import Workbook

import hashlib
import random
import io

from django.http.response import HttpResponse

from xlsxwriter.workbook import Workbook

from clients.forms import RegisterForm, ClientRegisterForm
from clients.models import Client

from clients.serializers import ClientSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin

import json


class ClientsListPhoto(ListModelMixin, viewsets.ViewSet):
    """
    A simple ViewSet for listing clients photo
    """
    def list(self):
        queryset = Client.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)


class ClientsListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "clients/clients_list_view.html"
    ordering = 'name'

    def add_like(self):
        dict = {}
        client_id = self.request.GET.get('client_id')
        dict['client_id'] = client_id
        like = self.request.GET.get('like')
        client = Client.objects.get(pk=client_id)
        client.likes = like
        dict['like'] = client.likes
        client.save()
        return JsonResponse(json.dumps(dict), content_type="application/json")

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ClientsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(ClientsListView, self).get_queryset()
        name = self.request.GET.get('name', None)
        if name:
            queryset = Client.objects.all().filter(
                (Q(name__icontains=name)) |
                (Q(surname__icontains=name))
            )

        return queryset

    def get_ordering(self):
        self.ordering = self.request.GET.get('order', 'value')
        order = self.request.GET.get('order', 'name')
        if self.ordering == 'value':
            order = "-" + order
        return order

    def get_context_data(self, *args, **kwargs):
        context = super(ClientsListView, self).get_context_data(*args, **kwargs)
        context['order'] = self.ordering
        return context

    def save_to_xlsx_format(self):
        output = io.BytesIO()

        workbook = Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        i = 0
        clients = Client.objects.all()
        q = Client()._meta
        q = [f.name for f in q.fields]

        worksheet.write(i, 0, q[2])
        worksheet.write(i, 1, q[3])
        worksheet.write(i, 2, q[4])

        for cl in clients:
            i += 1
            worksheet.write(i, 0, cl.name)
            worksheet.write(i, 1, cl.surname)
            worksheet.write(i, 2, str(cl.birth_Day))

        workbook.close()

        output.seek(0)

        response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = "attachment; filename=test.xlsx"

        return response


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
    success_url = '/clients/'

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


def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})


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
    return render(request, 'clients/client_add.html', {'form': form})



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