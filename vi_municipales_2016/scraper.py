# -*- coding: utf-8 -*-
from vi_municipales_2016.models import PosibleFacebookPage
import facebook
from django.conf import settings
TOKEN = settings.FACEBOOK_ACCESS_TOKEN


def string_for_search_generator(candidate):
    names = []
    name_without_last_surname = candidate.name.rsplit(' ', 1)[0]
    names.append(name_without_last_surname + u' ' + candidate.election.area.name)
    names.append(name_without_last_surname + u' ' + candidate.election.position)
    return names


class Scraper(object):
    def scrape(self, election):
        graph = facebook.GraphAPI(access_token=TOKEN, version='2.5')
        for candidate in election.candidates.all():
            strings = string_for_search_generator(candidate)
            for search in strings:
                result = graph.request('search', {'q': search, 'type': 'page'})
                for data in result['data']:
                    url = 'http://www.facebook.com/' + data['id']
                    page_name = data['name']
                    posible_page, created = PosibleFacebookPage.objects.get_or_create(url=url, name=page_name,
                            candidate=candidate)