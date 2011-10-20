from django.conf.urls.defaults import patterns, include, url
from gp_utils import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^feedback/', include('multisource_feedback.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

#urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gp_utils.views.home', name='home'),
    # url(r'^gp_utils/', include('gp_utils.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
#)
