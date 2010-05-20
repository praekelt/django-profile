from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from profile.models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(UserAdmin):
    inlines = [
        ProfileInline,
    ]

# Unregister default django User admin 
admin.site.unregister(User)

# Register our customized User admin 
admin.site.register(User, UserAdmin)
