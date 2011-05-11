# -*- coding: utf-8 -*-
from django.db import models

class Video(models.Model):
    name = models.CharField("Nome", max_length=200)
    desc = models.TextField("Descrição", null=True, blank=True)
    link = models.CharField("Link do Youtube", max_length=150)
