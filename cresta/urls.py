'''
urls.py
Cresta Flow System
http://www.codecresta.com
'''

from django.views.generic import TemplateView, RedirectView
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from flow import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^test404/$', TemplateView.as_view(template_name='404.html'), name="404"),
    url(r'^test500/$', TemplateView.as_view(template_name='500.html'), name="500"),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^admin/', admin.site.urls),
    url(r'^register/$', login_required(views.register), name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^list_flows/$', login_required(views.ListFlows.as_view()), name='list-flows'),
    url(r'^view_flow/(?P<flow_id>[0-9]+)/$', login_required(views.ViewFlow.as_view()), name='view-flow'),
    url(r'^create_flow/(?P<type_desc>\w+)/$', login_required(views.CreateFlow.as_view()), name='create-flow'),
    url(r'^update_flow/(?P<flow_id>[0-9]+)/(?P<version>[0-9]+)/$', login_required(views.update_flow),
        name='update-flow'),
    url(r'^delete_flow/(?P<flow_id>[0-9]+)/$', login_required(views.DeleteFlow.as_view()), name='delete-flow'),
    url(r'^list_flow_events/(?P<flow_id>[0-9]+)/$', login_required(views.ListFlowEvents.as_view()),
        name='list-flow-events'),
    url(r'^advance_flow/(?P<flow_id>[0-9]+)/(?P<version>[0-9]+)/$', login_required(views.advance_flow),
        name='advance-flow'),
    url(r'^revert_flow/(?P<flow_id>[0-9]+)/(?P<version>[0-9]+)/$', login_required(views.revert_flow),
        name='revert-flow'),
    url(r'^list_flow_logs/(?P<flow_id>[0-9]+)/$', login_required(views.ListFlowLogs.as_view()),
        name='list-flow-logs'),
    url(r'^create_log/(?P<flow_id>[0-9]+)/$', login_required(views.CreateLog.as_view()), name='create-log'),
)
