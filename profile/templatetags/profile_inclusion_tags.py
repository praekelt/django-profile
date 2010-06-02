from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.inclusion_tag('profile/inclusion_tags/avatar.html')
def avatar(username, width, height):
    try:
        profile = User.objects.get(username=username).profile
    except User.DoesNotExist:
        profile = None

    return {
        'profile': profile,
        'width': width,
        'height': height,
    }
