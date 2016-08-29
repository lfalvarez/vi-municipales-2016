# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View
from vi_municipales_2016.models import PosibleFacebookPage
from vi_municipales_2016.forms import CandidateFacebookPageForm
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from elections.models import Candidate
from django.views.generic.base import RedirectView
from elections.models import Election
from vi_municipales_2016.scraper import Scraper
from vi_municipales_2016.tasks import scrape_election, verify_facebook_page
from django.core.urlresolvers import reverse


class VerificarBase(View):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_staff:
            return HttpResponseNotFound('No encontrado')
        self.facebook_page = get_object_or_404(PosibleFacebookPage,
                                               id=self.kwargs['pk'])
        return super(VerificarBase, self).dispatch(request, *args, **kwargs)

    def process(self):
        pass

    def get(self, request, *args, **kwargs):
        self.process()
        return HttpResponseRedirect(self.facebook_page.candidate.get_absolute_url())


class VerificarSi(VerificarBase):
    def process(self):
        verify_facebook_page(self.facebook_page)


class VerificarNo(VerificarBase):
    def process(self):
        self.facebook_page.verified = False
        self.facebook_page.save()


class AgregarFacebookCandidato(FormView):
    form_class = CandidateFacebookPageForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        if not self.user.is_staff:
            return HttpResponseNotFound('No encontrado')
        self.candidate = get_object_or_404(Candidate, pk=self.kwargs['pk'])
        return super(AgregarFacebookCandidato, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.candidate.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(AgregarFacebookCandidato, self).get_form_kwargs()
        kwargs['candidate'] = self.candidate
        return kwargs

    def form_valid(self, form):
        form.validate_facebook_page()
        return super(AgregarFacebookCandidato, self).form_valid(form)


class ScrapeElectionView(RedirectView):
    permanent = False
    query_string = True

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        self.user = self.request.user
        if not self.user.is_staff:
            return HttpResponseNotFound('No encontrado')
        self.election = get_object_or_404(Election,
                                          slug=self.kwargs['slug'])
        return super(ScrapeElectionView, self).dispatch(*args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        scrape_election.delay(self.election)
        return reverse('election_view', kwargs={'slug': self.election.slug})