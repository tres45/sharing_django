from django import template
from chogori.models import Hike, Category


register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.inclusion_tag('chogori/tags/new_hike.html')
def get_new_hikes(count=5):
    hikes = Hike.objects.order_by('id').filter(draft=False)[:count]
    return {'new_hikes': hikes}
