from django.conf.urls import url
from clients import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='clients/login.html'),  name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='clients/index.html'),  name='logout'),
    url(r'^activate/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,32})/$', views.activate, name='activate'),
    url(r'^create_client/$', views.create_client, name='create_client'),
    url(r'^info_clients/$', views.InfoClients.as_view(), name='info_clients'),
    url(r'^info_clients/(?P<pk>[0-9]+)/$', views.ClientDetails.as_view(), name='info_clients'),
    url (r'^info_clients/(?P<pk>[0-9]+)/$', views.DeleteClient.as_view(), name='delete_clients'),
]
