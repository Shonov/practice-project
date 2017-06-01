from django.conf.urls import url
from clients import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='clients/login.html'),  name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='clients/index.html'), name='logout'),
]
