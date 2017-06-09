from django.conf.urls import url
from clients import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls import url
from mysite.search import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='clients/login.html'),  name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='clients/index.html'),  name='logout'),
    url(r'^activate/(?P<id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,32})/$', views.activate, name='activate'),
    url(r'^create_client/$', views.create_client, name='create_client'),
    url(r'^info_clients/$', views.ClientsListView.as_view(), name='clients_list_view'),
    url(r'^info_clients/$', views.ClientsListView.get_queryset, name='sort'),
    url(r'^info_clients/(?P<pk>[0-9]+)/$', views.ClientDetailView.as_view(), name='info_clients'),
    url(r'^info_clients/(?P<pk>[0-9]+)/delete/$', views.ClientDeleteView.as_view(), name='delete_clients'),
    url(r'^info_clients/(?P<pk>[0-9]+)/update/$', views.ClientUpdateView.as_view(), name='update_client'),
    url(r'^info_clients/$', views.search, name='search'),
    url(r'^search/$', views.search, name='search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
