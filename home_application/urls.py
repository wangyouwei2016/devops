# -*- coding: utf-8 -*-

from django.conf.urls import patterns

urlpatterns = patterns('home_application.views',
    (r'^$', 'index'),
    (r'^monitor/$', 'monitor'),
    (r'^operation/$', 'operation'),
    (r'^urllist/$', 'urllist'),
    (r'^elk/$', 'elk'),
    (r'^menu/$', 'menu'),
    (r'^apply/$', 'apply'),
    (r'^applylist/$', 'applylist'),
    (r'^testlist/$', 'testlist'),
    (r'^rollbacklist/$', 'rollbacklist'),
    (r'^returnedlist/$', 'returnedlist'),
    (r'^review/$', 'review'),
    (r'^package/$', 'package'),
    (r'^newapp/$', 'newapp'),
    (r'^applist/$', 'applist'),
    (r'^appoperation/$', 'appoperation'),
    (r'^dev-guide/$', 'dev_guide'),
    (r'^contactus/$', 'contactus'),
    (r'^header/$', 'header'),

            )
