# Create your views here.
from news.models import Notice
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from utils import ContextHackMixin
from django import forms
from django.shortcuts import get_object_or_404

class NoticeForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'mce'}))
    class Meta:
        model = Notice
        exclude = ('user',)

class NoticeList(ContextHackMixin, ListView):
    model = Notice
    paginate_by = 5

class NoticeAdd(ContextHackMixin, CreateView):
    model = Notice
    form_class = NoticeForm
    success_url = "/news/"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        return super(NoticeAdd, self).form_valid(self.object)

    def get_success_url(self):
        return self.success_url

class NoticeUpdate(ContextHackMixin, UpdateView):
    model = Notice
    form_class = NoticeForm
    success_url = "/news/"

class NoticeDelete(ContextHackMixin, DeleteView):
    model = Notice
    success_url = "/news/"

class NoticeView(ContextHackMixin, DetailView):
    model = Notice
