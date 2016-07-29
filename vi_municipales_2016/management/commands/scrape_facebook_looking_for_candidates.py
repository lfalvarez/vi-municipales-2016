# coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from ._candidates import CANDIDATES
from elections.models import Election
import facebook
from vi_municipales_2016.models import PosibleFacebookPage
from django.conf import settings

TOKEN = settings.FACEBOOK_ACCESS_TOKEN


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('election_id', type=int)

    def handle(self, *args, **options):
        graph = facebook.GraphAPI(access_token=TOKEN, version='2.5')
        election = Election.objects.get(id=options['election_id'])

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