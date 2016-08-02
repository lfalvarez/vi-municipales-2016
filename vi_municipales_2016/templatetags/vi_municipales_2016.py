from django import template
from ..forms import CandidateFacebookPageForm

register = template.Library()


@register.inclusion_tag('facebook_page_form.html', takes_context=True)
def facebook_page_form(context):
	form = CandidateFacebookPageForm(candidate=context['candidate'])
	context.update({'form': form})
	return context