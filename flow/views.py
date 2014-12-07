import math
from datetime import datetime
from django.utils import timezone
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import CreateView, ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from flow.models import Type, Flow, Event, Log
from flow.forms import UserForm, UserProfileForm, CustomFormA, CustomFormB, FlowForm, EventForm
from flow import utils

'''
if you need custom logging:
import logging

logger = logging.getLogger(__name__)
def render_error(scr_msg, err_msg, context):
    logger.debug(err_msg)
    return render_to_response('error.html', {'message': scr_msg}, context)
'''

'''
def in_group(user, group):
    return user.groups.filter(name=group).exists()
def in_group1(user):
    return in_group(user, 'group 1')
def in_group2(user):
    return in_group(user, 'group 2')
'''

# supporting functions
def dt_seconds(dt):
    tz = timezone.get_current_timezone()
    td = dt - tz.localize(datetime.strptime('1/1/2000', '%d/%m/%Y'), is_dst=None)
    return math.trunc(td.total_seconds())

def is_superuser(user):
    return user.is_superuser

def decode_url(u):
    return u.replace('_', ' ')

# create a user and a profile
def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    context_dict = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }
    return render_to_response('register.html', context_dict, context)

# fbv for user login
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('login.html', {}, context)

# login required decorator
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# render home page
def home(request):
    context = RequestContext(request)
    return render_to_response('home.html', {}, context)

# cbv for showing list of flows, the states shown depend on user's groups
class ListFlows(ListView):
    model = Flow
    queryset = Flow.objects.none()
    template_name = 'list_flows.html'
    context_object_name = 'flow_list'
    paginate_by = 25
    def get_context_data(self, **kwargs):
        context = super(ListFlows, self).get_context_data(**kwargs)
        context.update({
            'can_update': is_superuser(self.request.user),
            'can_revert': is_superuser(self.request.user),
            'can_delete': is_superuser(self.request.user)          
        })
        return context
    def get_queryset(self, **kwargs):
        wf = utils.Workflow()
        wf.init()
        queryset = Flow.objects.order_by('-modified')
        return queryset.filter(state__description__in=wf.get_user_states(self.request.user))

# cbv for viewing a single flow
class ViewFlow(DetailView):
    context_object_name = 'flow'
    model = Flow
    template_name = 'view_flow.html'
    slug_field = 'id'
    slug_url_kwarg = 'flow_id'
    def get_context_data(self, **kwargs):
        context = super(ViewFlow, self).get_context_data(**kwargs)
        context.update({
            'flow': get_object_or_404(Flow, id=self.kwargs['flow_id'])
        })
        return context

# cbv for creating a new flow
class CreateFlow(CreateView):
    model = Flow
    fields = ['ref', 'state']
    form_class = FlowForm
    template_name = 'create_flow.html'
    success_url = reverse_lazy('list-flows')
    def get_context_data(self, **kwargs):
        context = super(CreateFlow, self).get_context_data(**kwargs)
        context.update({
            'type_desc': self.kwargs['type_desc']
        })
        return context
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.flow_type = get_object_or_404(Type, description=decode_url(self.kwargs['type_desc']))
        self.object.version = 0
        self.object.save()
        self.object.version = dt_seconds(self.object.modified)
        result = super(CreateFlow, self).form_valid(form)
        event = Event(user=self.request.user, flow=self.object, state=self.object.state)
        event.save()
        return result

# fbv for updating a flow
@user_passes_test(is_superuser, login_url='/login/')
def update_flow(request, flow_id, version):
    context = RequestContext(request)
    flow = get_object_or_404(Flow, id=flow_id)
    show_list = False
    version_msg = False
    if request.method == 'POST':
        if 'cancel' in request.POST:
            show_list = True
        else:
            if str(flow.version) == version:
                flow.save()
                flow.version = dt_seconds(flow.modified)
                flow.ref = request.POST['ref']
                flow.save()
                show_list = True
            else:
                version_msg = True
    if show_list:
        return HttpResponseRedirect(reverse_lazy('list-flows'))
    context_dict = {
        'flow_id': flow_id,
        'version': version,
        'version_msg': version_msg,
        'ref': flow.ref,
    }
    return render_to_response('update_flow.html', context_dict, context)

# cbv for deleting flows
class DeleteFlow(DeleteView):
    model = Flow
    success_url = reverse_lazy('list-flows')
    template_name = 'delete_flow.html'
    context_object_name = 'flow'
    slug_field = 'id'
    slug_url_kwarg = 'flow_id'
    def post(self, request, *args, **kwargs):
        if 'cancel' in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(DeleteFlow, self).post(request, *args, **kwargs)
    @method_decorator(user_passes_test(is_superuser, login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteFlow, self).dispatch(request, *args, **kwargs)

# supporting function for advancing a flow
def custom_advance(request, flow_id, version, context, flow, name, CustomForm):
    show_list = False
    version_msg = False
    if request.method == 'POST':
        event_form = EventForm(data=request.POST, flow_id=flow_id)
        custom_form = CustomForm(data=request.POST)
        if 'cancel' in request.POST:
            show_list = True
        else:
            if custom_form.is_valid() and event_form.is_valid():
                if str(flow.version) == version:
                    event = event_form.save(commit=False)
                    flow.state = event.state
                    flow.save()
                    flow.version = dt_seconds(flow.modified)
                    flow.save()
                    event.flow = flow
                    event.user = request.user
                    event.save()
                    custom = custom_form.save(commit=False)
                    custom.event = event
                    custom.save()
                    show_list = True
                else:
                    version_msg = True
    else:
        event_form = EventForm(flow_id=flow_id)
        custom_form = CustomForm()
    context_dict = {name: custom_form}
    if show_list:
        return HttpResponseRedirect(reverse_lazy('list-flows'))
    context_dict.update({
        'flow_id': flow_id,
        'version': version,
        'event_form': event_form,
        'version_msg': version_msg
    })
    return render_to_response(name + '.html', context_dict, context)

# fbv for advancing a flow
def advance_flow(request, flow_id, version):
    context = RequestContext(request)
    flow = get_object_or_404(Flow, id=flow_id)
    if flow.state.description == 'state 1':
        return custom_advance(request, flow_id, version, context, flow,
            'custom_form_a', CustomFormA)
    else:
        return custom_advance(request, flow_id, version, context, flow,
            'custom_form_b', CustomFormB)

# fbv for reverting a flow
@user_passes_test(is_superuser, login_url='/login/')
def revert_flow(request, flow_id, version):
    context = RequestContext(request)
    flow = get_object_or_404(Flow, id=flow_id)
    show_list = False
    version_msg = False
    if request.method == 'POST':
        if 'cancel' in request.POST:
            show_list = True
        else:
            if str(flow.version) == version:
                event = Event.objects.filter(flow_id=flow_id).order_by('-created')[0]
                event.delete()
                event = Event.objects.filter(flow_id=flow_id).order_by('-created')[0]
                flow.state = event.state
                flow.save()
                flow.version = dt_seconds(flow.modified)
                flow.save()
                show_list = True
            else:
                version_msg = True
    if show_list:
        return HttpResponseRedirect(reverse_lazy('list-flows'))
    context_dict = {
        'flow_id': flow_id,
        'version_msg': version_msg
    }
    return render_to_response('revert_flow.html', context_dict, context)

# cbv for listing flow events
class ListFlowEvents(ListView):
    context_object_name = 'flow_events_list'
    queryset = Event.objects.none()
    template_name = 'list_flow_events.html'
    paginate_by = 25
    def get_context_data(self, **kwargs):
        context = super(ListFlowEvents, self).get_context_data(**kwargs)
        context.update({
            'flow': get_object_or_404(Flow, id=self.kwargs['flow_id'])
        })
        return context
    def get_queryset(self, **kwargs):
        queryset = Event.objects.order_by('created')
        return queryset.filter(flow__id=self.kwargs['flow_id'])

# cbv for listing flow logs
class ListFlowLogs(ListView):
    context_object_name = 'flow_logs_list'
    queryset = Log.objects.none()
    template_name = 'list_flow_logs.html'
    paginate_by = 4
    def get_context_data(self, **kwargs):
        context = super(ListFlowLogs, self).get_context_data(**kwargs)
        context.update({
            'flow': get_object_or_404(Flow, id=self.kwargs['flow_id'])
        })
        return context
    def get_queryset(self, **kwargs):
        queryset = Log.objects.order_by('created')
        return queryset.filter(flow__id=self.kwargs['flow_id'])

# cbv for creating logs
class CreateLog(CreateView):
    model = Log
    fields = ['content']
    template_name = 'create_log.html'
    def get_success_url(self):
        return reverse_lazy('list-flow-logs', kwargs={'flow_id': self.kwargs['flow_id']}) + '?page=last'
    def get_context_data(self, **kwargs):
        context = super(CreateLog, self).get_context_data(**kwargs)
        context.update({'flow_id': self.kwargs['flow_id']})
        return context
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.flow = get_object_or_404(Flow, id=self.kwargs['flow_id'])
        result = super(CreateLog, self).form_valid(form) 
        return result
