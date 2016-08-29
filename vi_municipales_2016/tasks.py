from votainteligente.celery import app
from vi_municipales_2016.scraper import Scraper
from votainteligente.facebook_page_getter import facebook_getter
# import the logging library
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


@app.task
def scrape_election(election):
    scraper = Scraper()
    scraper.scrape(election)


@app.task
def verify_facebook_page(facebook_page):
    facebook_page.verify()


@app.task
def verify(posible_facebook_page):
    result = facebook_getter(posible_facebook_page.url)
    posible_facebook_page.verified = True
    posible_facebook_page.save()
    
    posible_facebook_page.candidate.image = result['picture_url']
    posible_facebook_page.candidate.save()
    posible_facebook_page.candidate.add_contact_detail(contact_type='FACEBOOK',
                                      label=result['name'],
                                      value=posible_facebook_page.url)

