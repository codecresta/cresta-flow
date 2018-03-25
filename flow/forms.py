'''
forms.py
Cresta Flow System
http://www.codecresta.com
'''

from django import forms
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from flow.models import UserProfile, CustomA, CustomB, Flow, State, Event
from flow import utils

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'is_superuser', 'groups', 'is_staff', 'email', 'password']
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

class CustomFormA(forms.ModelForm):
    class Meta:
        model = CustomA
        fields = ['text']

class CustomFormB(forms.ModelForm):
    class Meta:
        model = CustomB
        fields = ['integer']

class FlowForm(forms.ModelForm):
    wf = utils.Workflow()
    wf.init()
    class Meta:
        model = Flow
        fields = ['state', 'ref']
    def __init__(self, *args, **kwargs):
        super(FlowForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.filter(description__in=self.wf.get_init_states())

class EventForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.none())
    wf = utils.Workflow()
    wf.init()
    class Meta:
        model = Event
        fields = ['state']
    def __init__(self, *args, **kwargs):
        flow_id = kwargs.pop('flow_id')
        flow = get_object_or_404(Flow, id=flow_id)
        state_desc = flow.state.description
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['state'].queryset = State.objects.filter(description__in=self.wf.get_trans(state_desc))

def get_cus_forms(wf):
    wf.app_cus_form('state 1', 'custom_form_a', CustomFormA)
    wf.app_cus_form('state 2', 'custom_form_b', CustomFormB)

    
