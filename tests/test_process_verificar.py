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
from popolo.models import Area, ContactDetail
from vi_municipales_2016.scraper import Scraper, string_for_search_generator
from vi_municipales_2016.forms import CandidateFacebookPageForm
import vcr
import os
from django.template.loader import get_template
from django.template import Template, Context
__dir__ = os.path.dirname(os.path.realpath(__file__))


@override_settings(THEME='vi_municipales_2016')
class ProcessTestCase(TestCase):
    def setUp(self):
        super(ProcessTestCase, self).setUp()
        self.candidate = Candidate.objects.get(id=1)
        self.feli.set_password('alvarez')
        self.feli.is_staff = True
        self.feli.save()

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/pablo_page2.yaml')
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

    def test_string_for_test_generator(self):
        valdivia = Area.objects.create(name='Valdivia')
        election = Election.objects.create(area=valdivia, name='Concejales')
        candidate = Candidate.objects.create(name='Pablo Moya',
                                             given_name='Pablo',
                                             family_name='Moya')
        election.candidates.add(candidate)
        names = string_for_search_generator(candidate)
        self.assertIn('Pablo Moya Valdivia', names)
        self.assertIn('Pablo Moya Concejales', names)
        self.assertIn('Pablo Valdivia', names)
        self.assertIn('Moya Valdivia', names)

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

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/matias_page.yaml')
    def test_post_page_for_candidate(self):
        url = reverse('agregar_facebook_a_candidato', kwargs={'pk': self.candidate.pk})
        self.client.login(username=self.feli.username, password='alvarez')
        data = {'page': 'https://www.facebook.com/matiasxvaldivia/?fref=ts'}
        response = self.client.post(url, data=data, follow=True)
        posible_page = PosibleFacebookPage.objects.get(candidate=self.candidate)
        self.assertIn(posible_page.url, data['page'])
        self.assertTrue(posible_page.verified)
        contact_detail = ContactDetail.objects.get(contact_type='FACEBOOK',
                                                   value=posible_page.url)
        self.assertIn(contact_detail, self.candidate.contact_details.all())

    def test_form_parse_facebook_url(self):
        data = {'page': 'https://www.facebook.com/matiasxvaldivia/?fref=ts'}
        form = CandidateFacebookPageForm(candidate=self.candidate, data=data)
        self.assertTrue(form.is_valid())
        self.assertEquals(form.cleaned_data['page'], 'matiasxvaldivia')

    def test_include_facebook_page_form(self):
        template_str = get_template('facebook_page_form.html')
        form = CandidateFacebookPageForm(candidate=self.candidate)
        rendered_template = template_str.render(Context({'form': form,
                                                         'candidate': self.candidate}))
        template = Template("{% load vi_municipales_2016 %}{% facebook_page_form %}")
        self.assertEqual(template.render(Context({'candidate': self.candidate})),
                         rendered_template)

    @vcr.use_cassette(__dir__ + '/fixtures/vcr_cassettes/pablo.yaml')
    def test_scrape_election_view(self):
        valdivia = Area.objects.create(name='Valdivia')
        election = Election.objects.create(area=valdivia, name='Concejales')
        candidate = Candidate.objects.create(name='Pablo Moya')
        election.candidates.add(candidate)
        url = reverse('scrape_election', kwargs={'slug': election.slug})
        self.client.login(username=self.feli.username, password='alvarez')
        response = self.client.get(url)
        election_url = reverse('election_view', kwargs={'slug': election.slug})
        self.assertRedirects(response, election_url)
        posible_page = PosibleFacebookPage.objects.get(candidate=candidate)
        self.assertIsNone(posible_page.verified)