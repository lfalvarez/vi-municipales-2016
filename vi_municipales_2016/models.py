# -*- coding: utf-8 -*-

from django.db import models
from elections.models import Candidate
from model_utils.models import TimeStampedModel
from votainteligente.facebook_page_getter import facebook_getter

class PosibleFacebookPage(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=512)
    candidate = models.ForeignKey(Candidate,
                                  default=None,
                                  null=True,
                                  related_name='posible_facebook_pages')
    verified = models.NullBooleanField(default=None)

    def verify(self):

    	print self.url
    	result = facebook_getter(self.url)
    	self.verified = True
    	self.save()
    	
    	self.candidate.image = result['picture_url']
    	self.candidate.save()
    	self.candidate.add_contact_detail(contact_type='FACEBOOK',
    									  label=result['name'],
    									  value=self.url)

class CandidateFacebookPage(TimeStampedModel):
    pass