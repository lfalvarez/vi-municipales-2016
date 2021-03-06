# -*- coding: utf-8 -*-
from django.conf.urls import url

from .views import VerificarSi, VerificarNo, AgregarFacebookCandidato, ScrapeElectionView

urlpatterns = [
    url(r'^verificar_si/(?P<pk>\d+)/$',
        VerificarSi.as_view(),
        name='verificar_si'),
    url(r'^verificar_no/(?P<pk>\d+)/$',
        VerificarNo.as_view(),
        name='verificar_no'),
    url(r'^agregar_facebook_a_candidato/(?P<pk>[-\w]+)/$',
        AgregarFacebookCandidato.as_view(),
        name='agregar_facebook_a_candidato'),
    url(r'^scrape_election/(?P<slug>[-\w]+)/$',
        ScrapeElectionView.as_view(),
        name='scrape_election'),
]