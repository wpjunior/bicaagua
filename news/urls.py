from django.conf.urls.defaults import patterns, include, url
from news.views import (NoticeList, NoticeAdd, NoticeUpdate, NoticeDelete, NoticeView)
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('news.views',
                       url(r'^$', NoticeList.as_view()),
                       url(r'^add/$', login_required(NoticeAdd.as_view())),
                       url(r'^edit/(?P<pk>\d+)/$', login_required(NoticeUpdate.as_view())),
                       url(r'^delete/(?P<pk>\d+)/$', login_required(NoticeDelete.as_view())),
                       url(r'^(?P<pk>\d+)/$', NoticeView.as_view()),
)
