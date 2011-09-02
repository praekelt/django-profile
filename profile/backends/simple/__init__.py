from django.contrib import messages
from django.utils.translation import ugettext

from registration import signals
from registration.backends.simple import SimpleBackend

from profile import utils


class SimpleBackend(SimpleBackend):
    def get_form_class(self, request):
        return utils.get_profile_model().registration_form

    def post_registration_redirect(self, request, user):
        """
        After registration, redirect to the next or
        otherwise user's absolute url.
        """
        return (self._get_redirect_url(request), (), {})

    def _get_redirect_url(self, request):
        """
        Next gathered from session, then GET, then POST,
        then users absolute url.
        """
        if 'next' in request.session:
            next = request.session['next']
            del request.session['next']
            return next
        elif 'next' in request.GET:
            return request.GET.get('next')
        elif 'next' in request.POST:
            return request.POST.get('next')
        else:
            return request.user.get_absolute_url()


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
