from django import forms
from django.forms import ModelForm

from profile.models import AbstractAvatarProfile, AbstractProfileBase, AbstractLocationProfile, AbstractContactProfile, AbstractPersonalProfile, AbstractSubscriptionProfile

from registration.forms import RegistrationForm

class SubscriptionsModelForm(ModelForm):
    class Meta:
        model = AbstractSubscriptionProfile

class SubscriptionsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SubscriptionsForm, self).__init__(*args, **kwargs)
        self.fields.update(SubscriptionsModelForm().fields)

class RegistrationFormSubscriptions(RegistrationForm, SubscriptionsForm):
    pass

class LocationModelForm(ModelForm):
    class Meta:
        model = AbstractLocationProfile

class LocationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(LocationForm, self).__init__(*args, **kwargs)
        self.fields.update(LocationModelForm().fields)

class PersonalModelForm(ModelForm):
    class Meta:
        model = AbstractPersonalProfile

class PersonalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PersonalForm, self).__init__(*args, **kwargs)
        self.fields.update(PersonalModelForm().fields)

class ContactModelForm(ModelForm):
    class Meta:
        model = AbstractContactProfile

class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.update(ContactModelForm().fields)

class ProfileBaseModelForm(ModelForm):
    class Meta:
        model = AbstractProfileBase

class ProfileBaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfileBaseForm, self).__init__(*args, **kwargs)
        self.fields.update(ProfileBaseModelForm().fields)

class AvatarModelForm(ModelForm):
    class Meta:
        model = AbstractAvatarProfile

class AvatarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AvatarForm, self).__init__(*args, **kwargs)
        self.fields.update(AvatarModelForm().fields)
