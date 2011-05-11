from django.conf.urls.defaults import patterns, include, url
from videos.views import VideoList, VideoCreate, VideoEdit, VideoDelete

urlpatterns = patterns('albuns.views',
    url(r'^$', VideoList.as_view()),
                       #TODO: require login
    url(r'^add/$', VideoCreate.as_view()),
    url(r'^(?P<pk>\d+)/$', VideoEdit.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', VideoDelete.as_view()),
    url(r'action/$', 'album_action'), #TODO require login
)
