# -*- coding: utf-8 -*-

from django.db import models
from elections.models import Candidate
from model_utils.models import TimeStampedModel
from vi_municipales_2016.tasks import verify

class PosibleFacebookPage(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=512)
    candidate = models.ForeignKey(Candidate,
                                  default=None,
                                  null=True,
                                  related_name='posible_facebook_pages')
    verified = models.NullBooleanField(default=None)

    def verify(self):
    	verify.delay(self)


class CandidateFacebookPage(TimeStampedModel):
    pass