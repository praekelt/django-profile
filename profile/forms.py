from registration.forms import RegistrationFormTermsOfService
from captcha.fields import ReCaptchaField

class RegistrationForm(RegistrationFormTermsOfService):
    recaptcha = ReCaptchaField(
        label="Human?",
    )
