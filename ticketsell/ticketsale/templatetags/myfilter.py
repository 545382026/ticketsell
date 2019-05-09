from django.template import Library

register = Library()

import datetime
@register.simple_tag
def get_current_time():
    time = datetime.datetime.now()
    time = time.strftime('%H:%M:%S')
    return ''.format(time)
