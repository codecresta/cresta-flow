'''
utils.py
Cresta Flow System
http://www.codecresta.com
'''

# class for managing workflow logic / structure
class Workflow:
    state_lists = {} # stores a list of states for each group
    state_trans = {} # stores a list of transition states for each state
    init_states = [] # stores a list of initial states
    term_states = [] # stores a list of terminal states
    cus_states = [] # custom form state description
    cus_names = [] # custom form html name
    cus_forms = [] # custom form
    # append a user group
    def app_group(self, group):
        self.state_lists[group] = []
    # append a state (made visible) to a group
    def app_group_state(self, group, state):
        self.state_lists[group].append(state)
    # get (visible) states for a particular user
    def get_user_states(self, user):
        result = []
        for key, value in self.state_lists.items():
            if (user.groups.filter(name=key).exists()):
                result.extend(value)
        return result
    # append a state
    def app_state(self, state):
        self.state_trans[state] = []
    # append a transition (state) to a state
    def app_trans(self, state, trans_state):
        self.state_trans[state].append(trans_state)
    # get the transitions (states) for a particular state
    def get_trans(self, state):
        return self.state_trans[state]
    # append an initial state
    def app_init_state(self, state):
        self.init_states.append(state)
    # get all initial states
    def get_init_states(self):
        return self.init_states
    # append a terminal state
    def app_term_state(self, state):
        self.term_states.append(state)
    # get all terminal states
    def get_term_states(self):
        return self.term_states
    # append a custom form
    def app_cus_form(self, state, name, form):
        self.cus_states.append(state)
        self.cus_names.append(name)
        self.cus_forms.append(form)
    # test / demo workflow system
    def init(self):
        self.app_group('group 1')
        self.app_group('group 2')
        self.app_group_state('group 1', 'state 1')
        self.app_group_state('group 2', 'state 2')
        self.app_group_state('group 2', 'state 3')
        self.app_group_state('group 2', 'state 4')
        self.app_state('state 1')
        self.app_state('state 2')
        self.app_trans('state 1', 'state 2')
        self.app_trans('state 2', 'state 3')
        self.app_trans('state 2', 'state 4')
        self.app_init_state('state 1')
        self.app_term_state('state 3')
        self.app_term_state('state 4')
