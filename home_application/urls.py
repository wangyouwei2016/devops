# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
    (r'^$', 'index'),
    (r'^apply/$', 'apply'),
(r'^applylist/$', 'applylist'),
(r'^monitor/$', 'monitor'),
(r'^operation/$', 'operation'),
(r'^urllist/$', 'urllist'),
(r'^elk/$', 'elk'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
)
