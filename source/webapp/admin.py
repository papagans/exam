from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from webapp.models import Foto

class ProfileInline(admin.StackedInline):
    model = Foto
    fields =['foto', 'subscribe', 'rating', 'user']


class UserProfileAdmin(UserAdmin):
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
# Register your models here.
