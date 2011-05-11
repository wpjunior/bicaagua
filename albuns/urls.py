from django.conf.urls.defaults import patterns, include, url
from albuns.views import AlbumList, AlbumCreate, AlbumView, AlbumEdit, AlbumUpload
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('albuns.views',
    url(r'^$', AlbumList.as_view()),
                       #TODO: require login
    url(r'^add/$', login_required(AlbumCreate.as_view())),
    url(r'^(?P<pk>\d+)/$', AlbumView.as_view()),
    url(r'^edit/(?P<pk>\d+)/$', login_required(AlbumEdit.as_view())),
    url(r'^upload/(?P<pk>\d+)/$', login_required(AlbumUpload.as_view())),
    url(r'^(?P<pk>\d+)/action/$', 'image_action'),
    url(r'^(?P<pk>\d+)/upload/$', 'upload'),
    url(r'action/$', 'album_action'),
)
