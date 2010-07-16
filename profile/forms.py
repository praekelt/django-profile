from datetime import date

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from profile.models import AbstractAvatarProfile, AbstractProfileBase, AbstractLocationProfile, AbstractContactProfile, AbstractPersonalProfile, AbstractSubscriptionProfile

from registration.forms import RegistrationForm

from datetime import datetime
from profile import utils
from django.contrib.auth.models import User

class UserProfileModel(User, utils.get_profile_model()):
    class Meta:
        abstract = True

class ProfileModelForm(ModelForm):
    class Meta:
        model = UserProfileModel

class ProfileForm(forms.Form):
    """
    This is the generic profile form which you can use for all your user profile forms.
    It takes care of setting and saving User and Pofile objects for the form. 
    You can provide it with field excludes to build specific forms, i.e. avatar change for, 
    subscriptions form etc.
    """
    # list of default field names that will be excluded
    default_field_excludes = [
        'crop_from',
        'date_joined',
        'date_taken',
        'effect',
        'groups',
        'id',
        'is_staff',
        'is_active',
        'is_superuser',
        'last_login',
        'user',
        'user_permissions',
        'view_count',
        'password',
    ]
    # if true fields with names in default_field_excludes will be excluded
    exclude_default_fields=True, 
    # list of field names that will be excluded in addition to default_field_excludes(if active) 
    excluded_fields=[]

    password1 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_("Password"),
        required=False,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=False),
        label=_("Password (again)"),
        required=False,
    )

    # 3 seperate fields for dob
    dob_day = forms.ChoiceField(
        label=_("Birth Day"),
        choices=([('', 'Day'),] + [(i,i) for i in range(1, 32)]),
        required=False,
    )
    dob_month = forms.ChoiceField(
        label=_("Birth Month"),
        choices=([('', 'Month'),] + [(i,i) for i in range(1, 13)]),
        required=False,
    )
    dob_year = forms.ChoiceField(
        label=_("Birth Year"),
        choices=([('', 'Year'),] + [(i,i) for i in reversed(range(datetime.now().year - 100, datetime.now().year - 4))]),
        required=False,
    )

    def __init__(self, profile, user, *args, **kwargs):
        """
        profile: profile object
        user: user object
        """
        # build form
        super(ProfileForm, self).__init__(*args, **kwargs)

        # set form members user and profile. 
        self.profile = profile
        self.user = user
        
        # build excludes list
        excludes = self.excluded_fields
        if self.exclude_default_fields:
            excludes = excludes + self.default_field_excludes

        # gather fields form model, excluding excludes
        fields = ProfileModelForm().fields
        for exclude in excludes:
            if fields.has_key(exclude):     
                del fields[exclude]

        # convert dob to 3 seperate fields
        if fields.has_key('dob'):
            del fields['dob']
        else:
            del self.fields['dob_day']
            del self.fields['dob_month']
            del self.fields['dob_year']
          
        # convert email CharField to EmailField
        fields['email'] = forms.EmailField(fields['email'])
        
        self.fields.update(fields)
    
    def get_initial(self, *args, **kwargs):
        """
        Gathers initial form values from user and profile objects
        suitable for using as form's initial data.
        """
        initial = {}
        for field in self.fields:
            value = None
            if hasattr(self.user, field):
                value = getattr(self.user, field)
            if hasattr(self.profile, field):
                value = getattr(self.profile, field)
            if value:
                initial.update({
                    field: value
                })

        if hasattr(self.profile, 'dob'):
            dob = self.profile.dob
            if dob:
                if 'dob_day' in self.fields:
                    initial.update({
                        'dob_day': dob.day
                    })
                if 'dob_month' in self.fields:
                    initial.update({
                        'dob_month': dob.month
                    })
                if 'dob_year' in self.fields:
                    initial.update({
                        'dob_year': dob.year
                    })

        return initial
        
    def save(self, *args, **kwargs):
        """
        This method should be called when is_valid is true to save 
        relevant fields to user and profile models.
        """
        for key, value in self.cleaned_data.items():
            if value != None:
                if hasattr(self.user, key):
                    setattr(self.user, key, value)
                if hasattr(self.profile, key):
                    setattr(self.profile, key, value)

        # set password
        if 'password1' in self.cleaned_data:
            if self.cleaned_data['password1']:
                self.user.set_password(self.cleaned_data['password1'])

        # set dob
        if 'dob_day' in self.cleaned_data and 'dob_month' in self.cleaned_data and 'dob_year' in self.cleaned_data:
            self.profile.dob = self._gen_dob()

        self.user.save()
        self.profile.save()
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use. Don't fail if users username is provided.  
        """
        user = None
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']

        if user:
            if user.username == self.user.username:
                return self.cleaned_data['username']

        raise forms.ValidationError(_("A user with that username already exists."))

    def _gen_dob(self):
        if 'dob_day' in self.cleaned_data and 'dob_month' in self.cleaned_data and 'dob_year' in self.cleaned_data:
            if ['', '', ''] == [self.cleaned_data['dob_day'], self.cleaned_data['dob_month'], self.cleaned_data['dob_year']]:
                return None
            else:
                return date(
                    year=int(self.cleaned_data['dob_year']),
                    month=int(self.cleaned_data['dob_month']),
                    day=int(self.cleaned_data['dob_day']),
                )
        
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        """
        if 'dob_day' in self.cleaned_data and 'dob_month' in self.cleaned_data and 'dob_year' in self.cleaned_data:
                try:
                    self._gen_dob()
                except ValueError:
                    self._errors['dob_day'] = (_("You provided an invalid date."),)
        
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
       
        
        return self.cleaned_data

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
