from django.contrib import admin
from .models import Event, Comment, UserProfile, Photo


# Register your models here.
admin.site.register(Event)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Photo)