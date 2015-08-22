from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib import admin
import django.views.generic
admin.autodiscover()
import rest_framework


urlpatterns = [
    url(r'^$', views.url_list, name='urlexpand'),
    url(r'^urlexpand/(?P<pk>[0-9]+)/$', views.url_detail, name='urldetails'),
    url(r'^urlexpand/new/$', views.url_add, name='urladd'),
    url(r'^urlexpand/remove/(?P<pk>[0-9]+)/$', views.url_remove, name='url_remove'),
    url(r'^urlexpand/accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^urlexpand/accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/urlexpand'}),
    url(r'^api/$', views.rest_url_list, name='url-list'),
    url(r'^api/(?P<pk>[0-9]+)/$', views.rest_url_detail, name='url-detail'),
    url(r'^newimage/(?P<pk>[0-9]+)/$', views.newimage, name='url-newimage')
]
