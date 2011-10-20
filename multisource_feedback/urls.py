from django.conf.urls.defaults import *
from gp_utils import settings

urlpatterns = patterns('multisource_feedback.views',
    (r'^$', 'index'),
    (r'^logout/$', 'logout_user'),
    (r'^login/$', 'login_user'),
    (r'^login/submit/$', 'submit_login'),
    (r'^evaluate/$', 'evaluate_choose_member'),
    (r'^evaluate/(?P<member_id>\d+)/$', 'evaluate_member'),
    (r'^evaluate/(?P<member_id>\d+)/submit/$', 'submit_feedback'),
    (r'^view/$', 'choose_set'),
    (r'^view/(?P<set_id>\d+)/$', 'view_set'),
    (r'^view/(?P<set_id>\d+)/export/$', 'export_set'),
    (r'^view/(?P<set_id>\d+)/(?P<member_id>\d+)/$', 'view_one'),   
    (r'^view/(?P<set_id>\d+)/(?P<member_id>\d+)/export/$', 'export_member'),   
)