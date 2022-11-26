from django.contrib import admin

from .models import User, Trip, State, Achievement

# Register your models here.

admin.site.register(User)
admin.site.register(Trip)
admin.site.register(State)
admin.site.register(Achievement)