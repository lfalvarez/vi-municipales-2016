from votainteligente.celery import app
from vi_municipales_2016.scraper import Scraper
# import the logging library
import logging


# Get an instance of a logger
logger = logging.getLogger(__name__)


@app.task
def scrape_election(election):
    scraper = Scraper()
    scraper.scrape(election)
