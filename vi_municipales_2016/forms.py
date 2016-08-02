from django import forms
from vi_municipales_2016.models import PosibleFacebookPage
from urlparse import urlparse


class CandidateFacebookPageForm(forms.Form):
    page = forms.CharField()

    def __init__(self, candidate, *args, **kwargs):
        self.candidate = candidate
        super(CandidateFacebookPageForm, self).__init__(*args, **kwargs)

    def validate_facebook_page(self):
        possible_page = PosibleFacebookPage.objects.create(candidate=self.candidate)
        possible_page.url = self.cleaned_data['page']
        possible_page.save()
        possible_page.verify()

    def clean(self):
        cleaned_data = super(CandidateFacebookPageForm, self).clean()
        p = urlparse(cleaned_data['page'])
        cleaned_data['page'] = p.path.strip('/')
        return cleaned_data

    class Meta:
        labels = {'page': 'Pagina de Facebook'}