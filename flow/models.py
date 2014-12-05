from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
# from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to=settings.USER_PICS_DIR, blank=True)
    def __str__(self):
        return self.user.username

class Type(models.Model):
    description = models.CharField(max_length=32)
    def __str__(self):
        return self.description
    
class State(models.Model):
    description = models.CharField(max_length=32)
    def __str__(self):
        return self.description

class Flow(models.Model):
    ref = models.CharField(max_length=32)
    state = models.ForeignKey(State)
    flow_type = models.ForeignKey(Type)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    modified = models.DateTimeField(db_index=True, auto_now=True)
    version = models.IntegerField()
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
    user = models.ForeignKey(User)
    flow = models.ForeignKey(Flow)
    state = models.ForeignKey(State)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    def __str__(self):
        return str(self.id)

class Log(models.Model):
    user = models.ForeignKey(User)
    flow = models.ForeignKey(Flow)
    content = models.CharField(max_length=256)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    def __str__(self):
        return str(self.id)

class CustomA(models.Model):
    event = models.ForeignKey(Event)
    text = models.CharField(max_length=256)
    def __str__(self):
        return str(self.id)

class CustomB(models.Model):
    event = models.ForeignKey(Event)
    integer = models.IntegerField()
    def __str__(self):
        return str(self.id)
