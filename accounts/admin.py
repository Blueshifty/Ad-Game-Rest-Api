from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User
