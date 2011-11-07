#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from news.models import Notice
from albuns.models import Album
from bicaagua.captcha.fields import CaptchaField
from django.core.mail import send_mail, BadHeaderError
from django import forms
from bicaagua.settings import FROM_EMAIL, TO_EMAIL
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    notices = Notice.objects.all()[:5]

    return render_to_response("home.html", locals(),
                              context_instance=RequestContext(request))

class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=100)
    telefone = forms.CharField(max_length=10)
    email = forms.EmailField()
    mensagem = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField(label="Confirmação")

def faleconosco(request):

    if request.method == "POST":
        form = ContatoForm(request.POST)
    else:
        form = ContatoForm()

    if form.is_valid():
        nome = request.POST['nome']
        telefone = request.POST['telefone']
        email = request.POST['email']
        mensagem = request.POST['mensagem']

        t = loader.get_template('faleconosco_email.txt')
        c = Context(locals())
        text = t.render(c)

        print text

        try:
            send_mail("Mensagem FaleConosco", text, FROM_EMAIL, [TO_EMAIL])
        except:
            erro = 'Erro ao Enviar Mensagem'
        else:
            return HttpResponseRedirect('/')

    return render_to_response("faleconosco.html", locals(),
                              context_instance=RequestContext(request))
