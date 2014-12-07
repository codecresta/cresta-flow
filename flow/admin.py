'''
admin.py
Cresta Flow System
http://www.codecresta.com
'''

from django.contrib import admin
from flow.models import Type, State, Flow, Event, Log, UserProfile

admin.site.register(Type)
admin.site.register(State)
admin.site.register(Flow)
admin.site.register(Event)
admin.site.register(Log)
admin.site.register(UserProfile)
