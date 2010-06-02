from django.conf import settings
from django.contrib.auth.models import SiteProfileNotAvailable

def get_profile_model():
    auth_profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', None)
    profile_model = None
    if auth_profile_module:
        # get the profile model. TODO: super flacky, refactor
        app_label, model = auth_profile_module.split('.')
        profile_model = getattr(__import__("%s.models" % app_label, globals(), locals(), [model,], -1), model, None)

    if profile_model:
        return profile_model
    else:
        raise SiteProfileNotAvailable
