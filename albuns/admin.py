from django.contrib import admin
from django.contrib.contenttypes import generic
from albuns.models import Album, Photo
#from django.contrib.flatpages.models import FlatPage
#from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

"""
class FlatPageAdmin(FlatPageAdminOld):
    class Media:
        js = ('js/jquery-1.5.min.js',
              'js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

class NoticiaAdmin(admin.ModelAdmin):
    model = Noticia
    list_display = ('name', 'date')

    class Media:
        js = ('js/jquery-1.5.min.js',
              'js/tiny_mce/tiny_mce.js',
              'js/tiny_mce/textareas.js',)

"""

class PhotoAdmin(generic.GenericTabularInline):
    model = Photo

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'local', 'desc', 'date')
    inlines = [PhotoAdmin,]

#admin.site.unregister(FlatPage)
#admin.site.register(FlatPage, FlatPageAdmin)
#admin.site.register(Evento)
admin.site.register(Album, AlbumAdmin)
#admin.site.register(Noticia, NoticiaAdmin)
