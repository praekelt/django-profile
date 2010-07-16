from django.conf import settings

def get_profile_model():
    """
    Returns configured user profile model or None if not found
    """
    auth_profile_module = getattr(settings, 'AUTH_PROFILE_MODULE', None)
    profile_model = None
    if auth_profile_module:
        # get the profile model. TODO: super flacky, refactor
        app_label, model = auth_profile_module.split('.')
        profile_model = getattr(__import__("%s.models" % app_label, globals(), locals(), [model,], -1), model, None)

    return profile_model
