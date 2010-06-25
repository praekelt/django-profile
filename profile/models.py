from django.contrib.auth.models import User
from django.db import models

from photologue.models import ImageModel

class AbstractProfileBase(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey(
        User, 
        unique=True
    )
    
    def __unicode__(self):
        return self.user.username
    
class AbstractAvatarProfile(ImageModel):
    class Meta:
        abstract = True

class AbstractSocialProfile(models.Model):
    class Meta:
        abstract = True
    
    facebook_id = models.CharField(
        max_length=128,
        blank=True, 
        null=True,
    )
    twitter_username = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    @property
    def facebook_url(self):
        if self.facebook_id:
            return "http://www.facebook.com/profile.php?id=%s" % self.facebook_id
        else:
            return None
    
    @property
    def twitter_url(self):
        if self.twitter_username:
            return "http://www.twitter.com/%s" % self.twitter_username
        else:
            return None

class AbstractLocationProfile(models.Model):
    class Meta:
        abstract = True
    
    address = models.TextField(
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )
    province = models.CharField(
        max_length=256,
        blank=True,
        null=True,
    )

class AbstractPersonalProfile(models.Model):
    class Meta:
        abstract = True
    
    dob = models.DateField(
        verbose_name="Date of Birth",
        blank=True,
        null=True,
    )

class AbstractContactProfile(models.Model):
    class Meta:
        abstract = True
   
    mobile_number = models.CharField(
        max_length=64,
        blank=True,
        null=True,
    )

class AbstractSubscriptionProfile(models.Model):
    class Meta:
        abstract = True
    
    receive_sms = models.BooleanField(
        default=False,
    )
    receive_email = models.BooleanField(
        default=False,
    )

class AbstractWebuserProfile(AbstractProfileBase, AbstractAvatarProfile, AbstractContactProfile, AbstractLocationProfile, AbstractPersonalProfile, AbstractSocialProfile, AbstractSubscriptionProfile):
    class Meta:
        abstract = True
