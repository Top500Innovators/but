# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'index', 'researchers.views.index', name='index'),
    url(r'comment/(?P<code>\d{8,100})?', 'researchers.views.comment', name='comment'),
    url(r'homepage/(?P<code>\d{8,100})$', 'researchers.views.homepage', name='homepage'),
    url(r'search/(?P<code>\d{8,100})$', 'researchers.views.search', name='search'),
    url(r'test/(?P<code>\d{8,100})$', 'researchers.views.test_search', name='test'),
    url(r'invite/(?P<code>\d{8,100})$', 'researchers.views.invite', name='invite'),
    url(r'update/(?P<code>\d{8,100})$', 'researchers.views.update', name='update'),
    url(r'join/(?P<code>\d{8,100})$', 'researchers.views.join', name='join'),                   
)
