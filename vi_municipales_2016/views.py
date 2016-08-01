# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View
from vi_municipales_2016.models import PosibleFacebookPage
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

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