from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(
        User, 
        unique=True
    )
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

    def __unicode__(self):
        return self.user.username
  
# Create User profile property which gets or creates an empty profile for the given user
User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
