from registration.backends.simple import SimpleBackend
from django.contrib import messages
from django.utils.translation import ugettext

from registration import signals

from profile import utils

class SimpleBackend(SimpleBackend):
    def get_form_class(self, request):
        return utils.get_profile_model().registration_form

def user_registered(sender, user, request, *args, **kwargs):
    profile = user.profile
    for field in request.POST:
        if hasattr(user, field):
            setattr(user, field, request.POST.get(field))
        if hasattr(profile, field):
            setattr(profile, field, request.POST.get(field))

    user.save()
    profile.save()

    msg = ugettext("You have signed up successfully.")
    messages.success(request, msg, fail_silently=True)

signals.user_registered.connect(user_registered)
