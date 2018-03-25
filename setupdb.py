'''
Run this file using:
> python setupdb.py
to set up initial data on the database.
'''

import os
import django

# supporting functions
def add_group(name):
    group = Group.objects.create()
    group.name = name
    group.save()

def add_type(description):
    ty = Type.objects.create()
    ty.description = description
    ty.save()

def add_state(description):
    state = State.objects.create()
    state.description = description
    state.save()

# set up Django and create records, must match definitions in Workflow class!
if __name__ == '__main__':
    print("Starting Django set up script, creating records...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cresta.settings')
    django.setup()
    from flow.models import Type, State
    from django.contrib.auth.models import Group
    add_type('type 1')
    add_state('state 1')
    add_state('state 2')
    add_state('state 3')
    add_state('state 4')
    add_group('group 1')
    add_group('group 2')
    for ty in Type.objects.all():
        print("Type: {0}".format(str(ty.description)))
    for state in State.objects.all():
        print("State: {0}".format(str(state.description)))
    for group in Group.objects.all():
        print("Group: {0}".format(str(group.name)))
