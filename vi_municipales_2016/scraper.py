# -*- coding: utf-8 -*-
from vi_municipales_2016.models import PosibleFacebookPage
import facebook
from django.conf import settings
TOKEN = settings.FACEBOOK_ACCESS_TOKEN


class Scraper(object):
    def scrape(self, election):
        graph = facebook.GraphAPI(access_token=TOKEN, version='2.5')
        for candidate in election.candidates.all():
            comuna = election.area.name
            candidate_name = candidate.name
            # cargo = candidate[2]
            search = candidate_name + u' ' + comuna
            result = graph.request('search', {'q': search, 'type': 'page'})
            for data in result['data']:
                url = 'http://www.facebook.com/' + data['id']
                page_name = data['name']
                posible_page, created = PosibleFacebookPage.objects.get_or_create(url=url, name=page_name,
                        candidate=candidate)
                print data['name'] + u'- http://www.facebook.com/' + data['id']