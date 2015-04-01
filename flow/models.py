'''
models.py
Cresta Flow System
http://www.codecresta.com
'''

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
#from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=False, null=False)
    picture = models.ImageField(upload_to=settings.USER_PICS_DIR, blank=True, null=True)
    def __str__(self):
        return self.user.username

class Type(models.Model):
    description = models.CharField(max_length=32, blank=False, null=False)
    def __str__(self):
        return self.description
    
class State(models.Model):
    description = models.CharField(max_length=32, blank=False, null=False)
    def __str__(self):
        return self.description

class Flow(models.Model):
    ref = models.CharField(max_length=32, blank=False, null=False)
    state = models.ForeignKey(State, blank=False, null=False)
    flow_type = models.ForeignKey(Type, blank=False, null=False)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(db_index=True, auto_now=True)
    version = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return str(self.id)
    '''
    def save(self, *args, **kwargs):
        if not self.created:
            self.created = timezone.now()
            # self.created = datetime.now().replace(tzinfo=get_current_timezone())
        self.modified = timezone.now()
        # self.modified = datetime.now().replace(tzinfo=get_current_timezone())
        return super(Flow, self).save(*args, **kwargs)
    '''
    
class Event(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    flow = models.ForeignKey(Flow, blank=False, null=False)
    state = models.ForeignKey(State, blank=False, null=False)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Log(models.Model):
    user = models.ForeignKey(User, blank=False, null=False)
    flow = models.ForeignKey(Flow, blank=False, null=False)
    content = models.CharField(max_length=256, blank=False, null=False)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    def __str__(self):
        return str(self.id)

class CustomA(models.Model):
    event = models.ForeignKey(Event, blank=False, null=False)
    text = models.CharField(max_length=256, blank=False, null=False)
    def __str__(self):
        return str(self.id)

class CustomB(models.Model):
    event = models.ForeignKey(Event, blank=False, null=False)
    integer = models.IntegerField(blank=False, null=False)
    def __str__(self):
        return str(self.id)
