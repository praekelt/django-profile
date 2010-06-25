from django.contrib.auth.models import SiteProfileNotAvailable
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import class_prepared

from django.conf import settings
    
auth_profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', None)
if not auth_profile_module:
    raise ImproperlyConfigured("You must provide an AUTH_PROFILE_MODULE setting.")
    
# connect profile property to User model  
def connect_profile(sender, **kwargs):
    from profile import utils
    try:
        profile_model = utils.get_profile_model()
    except SiteProfileNotAvailable:
        profile_model = None
    if profile_model:
        from django.contrib.auth.models import User
        User.profile = property(lambda u: profile_model.objects.get_or_create(user=u)[0])

class_prepared.connect(connect_profile,)
