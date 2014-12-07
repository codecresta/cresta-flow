'''
tests.py
Cresta Flow System
http://www.codecresta.com
'''

from django.test import TestCase
from django.contrib.auth.models import User
from flow.models import Type, State, Flow, Event, Log

import warnings
warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')

class FlowTestCases(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            username='temp',
            email='temp@gmail.com',
            password='temp'
        )
        user.is_superuser=True
        user.save()
        test_type = Type.objects.create(description='type 1')
        test_state = []
        for i in range(4):
            test_state.append(State.objects.create(description='state ' + str(i + 1)))
        test_flow = Flow.objects.create(
            ref='test flow',
            state=test_state[0],
            flow_type=test_type,
            version=0
        )
    def test_urls(self):
        self.client.login(username='temp', password='temp')
        response = self.client.get('/list_flows/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('flow_list' in response.context)
        response = self.client.get('/view_flow/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/create_flow/type_1/state_1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/update_flow/1/0/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/delete_flow/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/delete_flow/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/list_flow_events/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/advance_flow/1/0/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/revert_flow/1/0/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/list_flow_logs/1/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/create_log/1/')
        self.assertEqual(response.status_code, 200)
