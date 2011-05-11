#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from settings import MEDIA_ROOT
from stdimage import StdImageField

class PhotoManager(models.Manager):
    def get_all_related(self, object):
        type = ContentType.objects.get_for_model(object)
        return super(PhotoManager, self).get_query_set().filter(content_type__pk=type.id,
                                                                object_id=object.id)

class Photo(models.Model):
    name = models.CharField("Nome", max_length=100)
    image = StdImageField("Fotos", upload_to='photos', size=(800, 600), thumbnail_size=(200, 200, True))
    width = models.IntegerField(default=0)
    heigth = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, related_name="photo_content_type")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey("content_type", "object_id")
    objects = PhotoManager()

    def delete_files(self):
        filename = self.image.path
        if os.path.exists(filename):
            os.remove(filename)
        thumbnail_filename = self.image.thumbnail.path()
        if os.path.exists(thumbnail_filename):
            os.remove(thumbnail_filename)

    class Meta:
        db_table = "django_photo"

class Album(models.Model):
    name = models.CharField("Nome", max_length=100)
    local = models.CharField("Local", max_length=150)
    desc = models.TextField("Descrição")
    date = models.DateField("Data")

    class Meta:
        verbose_name = "Album"
        verbose_name_plural = "Albuns"
        db_table = "django_album"
        ordering = ['-date']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/albuns/%d/" % self.id

    def get_all_photos(self):
        return Photo.objects.get_all_related(self)

    def get_first_photo_thumbnail(self):
        a = Photo.objects.get_all_related(self)
        if a:
            return a[0].image.thumbnail.url()
        else:
            return "/media/img/nophoto.jpg"
