# Create your views here.
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.template import RequestContext
from videos.models import Video
from utils import JSONResponse, ContextHackMixin
from django.http import Http404
from django import forms

class VideoForm(forms.ModelForm):
    link = forms.RegexField(label="Link do Youtube",
                            regex=r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})",
                            error_messages={'invalid': 'Por Favor utilize um link valido'})
    class Meta:
        model = Video

class VideoList(ContextHackMixin, ListView):
    model = Video

class VideoCreate(ContextHackMixin, CreateView):
    model = Video
    form_class = VideoForm
    success_url = "/videos/"

class VideoEdit(ContextHackMixin, UpdateView):
    model = Video
    form_class = VideoForm
    success_url = "/videos/"

class VideoDelete(ContextHackMixin, DeleteView):
    model = Video
    success_url = "/videos/"
