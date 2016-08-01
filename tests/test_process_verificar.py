#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_vi-municipales-2016
------------

Tests for `vi-municipales-2016` models module.
"""
from django.core.urlresolvers import reverse
from popular_proposal.tests import ProposingCycleTestCaseBase as TestCase
from vi_municipales_2016.models import PosibleFacebookPage
from elections.models import Candidate, Election
from django.test import override_settings
from popolo.models import Area
from vi_municipales_2016.scraper import Scraper
import vcr
import os
__dir__ = os.path.dirname(os.path.realpath(__file__))


@override_settings(THEME='vi_municipales_2016')
class ProcessTestCase(TestCase):
    def setUp(self):
        super(ProcessTestCase, self).setUp()
        self.candidate = Candidate.objects.get(id=1)
        self.feli.set_password('alvarez')
        self.feli.is_staff = True
        self.feli.save()

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/pablo_page.yaml')
    def test_validate_si(self):
        posible_page = PosibleFacebookPage.objects.create(candidate=self.candidate,
                                                          url='https://www.facebook.com/PabloMoyaConcejal/',
                                                          name='possible page of the candidate')
        url = '/theme/verificar_si/' + str(posible_page.id)
        self.client.login(username=self.feli.username, password='alvarez')
        response = self.client.get(url, follow=True)

        self.assertEquals(response.status_code, 200)
        posible_page = PosibleFacebookPage.objects.get(id=posible_page.id)
        self.assertTrue(posible_page.verified)

    def test_validate_no(self):
        posible_page = PosibleFacebookPage.objects.create(candidate=self.candidate,
                                                          url='http://facebook.com',
                                                          name='possible page of the candidate')
        url = '/theme/verificar_no/' + str(posible_page.id)
        self.client.login(username=self.feli.username, password='alvarez')
        response = self.client.get(url, follow=True)

        self.assertEquals(response.status_code, 200)
        posible_page = PosibleFacebookPage.objects.get(id=posible_page.id)
        self.assertFalse(posible_page.verified)

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/pablo.yaml')
    def test_scrapea_al_amigo(self):
        valdivia = Area.objects.create(name='Valdivia')
        election = Election.objects.create(area=valdivia, name='Concejales')
        candidate = Candidate.objects.create(name='Pablo Moya')
        election.candidates.add(candidate)
        scraper = Scraper()
        scraper.scrape(election)
        posible_page = PosibleFacebookPage.objects.get(candidate=candidate)
        self.assertIsNone(posible_page.verified)

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/pablo_page.yaml')
    def test_get_data_and_include_it_into_the_candidate(self):
        posible_page = PosibleFacebookPage.objects.create(candidate=self.candidate,
                                                          url='https://www.facebook.com/PabloMoyaConcejal/',
                                                          name='Pablo Moya Concejal por Valdivia')
        posible_page.verify()
        posible_page = PosibleFacebookPage.objects.get(id=posible_page.id)
        self.assertTrue(posible_page.candidate.image)