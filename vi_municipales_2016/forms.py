from django import forms
from vi_municipales_2016.models import PosibleFacebookPage

class CandidateFacebookPageForm(forms.Form):
    page = forms.URLField()

    def __init__(self, candidate, *args, **kwargs):
    	self.candidate = candidate
    	super(CandidateFacebookPageForm, self).__init__(*args, **kwargs)

    def validate_facebook_page(self):
    	possible_page = PosibleFacebookPage.objects.create(candidate=self.candidate)
    	possible_page.url = self.cleaned_data['page']
    	possible_page.save()
    	possible_page.verify()