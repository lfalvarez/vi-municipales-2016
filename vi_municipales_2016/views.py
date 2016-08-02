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
        self.facebook_page.verify()


class VerificarNo(VerificarBase):
    def process(self):
        self.facebook_page.verified = False
        self.facebook_page.save()


class AgregarFacebookCandidato(FormView):
    form_class = CandidateFacebookPageForm

    def dispatch(self, *args, **kwargs):
        self.candidate = get_object_or_404(Candidate, pk=self.kwargs['pk'])
        return super(AgregarFacebookCandidato, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return self.candidate.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(AgregarFacebookCandidato, self).get_form_kwargs()
        kwargs['candidate'] = self.candidate
        return kwargs

    def form_valid(self, form):
        form.validate_facebook_page()
        return super(AgregarFacebookCandidato, self).form_valid(form)