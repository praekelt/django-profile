from registration.backends.default import DefaultBackend

from profile.forms import RegistrationForm

class DefaultBackend(DefaultBackend):
    def get_form_class(self, request):
        return RegistrationForm
