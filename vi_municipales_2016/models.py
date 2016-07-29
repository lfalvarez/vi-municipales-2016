# -*- coding: utf-8 -*-

from django.db import models
from elections.models import Candidate
from model_utils.models import TimeStampedModel


class PosibleFacebookPage(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=512)
    candidate = models.ForeignKey(Candidate,
                                  default=None,
                                  null=True,
                                  related_name='posible_facebook_pages')
    verified = models.NullBooleanField(default=None)

class CandidateFacebookPage(TimeStampedModel):
    pass
    


