'''
app_extras.py
Cresta Flow System
http://www.codecresta.com
'''

from django.conf import settings
from datetime import datetime
from django import template
from django.utils import timezone
from django.utils.timezone import localtime

register = template.Library()

@register.simple_tag
def project_name():
    return settings.PROJECT_NAME

@register.simple_tag
def company_name():
    return settings.COMPANY_NAME

@register.simple_tag
def meta_description():
    return settings.META_DESCRIPTION

@register.simple_tag
def meta_keywords():
    return settings.META_KEYWORDS

@register.simple_tag
def rowcolour(dt):
    diff = timezone.now() - dt
    if diff.days > 0:
        return "old_row"
    else:
        return "new_row"

@register.simple_tag
def page_link(curr_page, num_pages, offset):
    page = curr_page + offset
    if page >= 1 and page <= num_pages:
        page_str = str(page)
        return '<a href="?page=' + page_str + '">' + page_str + '</a>'
    else:
        return '<!-- Page number not relevant. -->'

@register.simple_tag
def encode_url(text):
    return text.replace(' ', '_')

'''
@register.simple_tag
def dt_seconds(dt):
    tz = timezone.get_current_timezone()
    td = dt - tz.localize(datetime.strptime('1/1/2000', '%d/%m/%Y'), is_dst=None)
    return math.trunc(td.total_seconds()
'''
