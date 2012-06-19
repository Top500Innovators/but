# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.simple import redirect_to
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^but/', include('researchers.urls')),
    url(r'^notices/', include('notification.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                           'document_root': settings.MEDIA_ROOT,
                           }),
 #   url(r'm/', include('mobile.urls')),
    url(r'', redirect_to, {'url': '/but/index'}),
)
urlpatterns += staticfiles_urlpatterns()

