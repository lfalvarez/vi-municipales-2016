# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from .views import VerificarSi, VerificarNo

urlpatterns = [
    url(r'^verificar_si/(?P<pk>\d+)/$',
        VerificarSi.as_view(),
        name='verificar_si'),
    url(r'^verificar_no/(?P<pk>\d+)/$',
        VerificarNo.as_view(),
        name='verificar_no'),
	]
