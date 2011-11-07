from django.conf.urls.defaults import patterns, include, url
from settings import MEDIA_ROOT
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^auth/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^auth/login/$', 'django.contrib.auth.views.login'),
    url(r'^media/(.*)','django.views.static.serve',{'document_root':MEDIA_ROOT}),
    url(r'^$', 'bicaagua.views.home', name='home'),
    url(r'^faleconosco/$', 'bicaagua.views.faleconosco', name='faleconosco'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^news/', include('bicaagua.news.urls')),
    url(r'^albuns/', include('bicaagua.albuns.urls')),
    url(r'^videos/', include('bicaagua.videos.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
