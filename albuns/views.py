# Create your views here
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView

from albuns.models import Album, Photo
from utils import JSONResponse, ContextHackMixin
from django.http import Http404
from django import forms
from django.contrib.auth.decorators import login_required

class AlbumForm(forms.ModelForm):
    date = forms.DateField(label="Data",
                           input_formats=("%d/%m/%Y",),
                           widget=forms.DateTimeInput(format='%d/%m/%Y', attrs={
                'class':'input',
                'readonly':'readonly',
                'size':'15'
                }))
    class Meta:
        model = Album

class AlbumList(ContextHackMixin, ListView):
    model = Album

class AlbumCreate(ContextHackMixin, CreateView):
    model = Album
    form_class = AlbumForm

class AlbumEdit(ContextHackMixin, UpdateView):
    model = Album
    form_class = AlbumForm

class AlbumView(ContextHackMixin, DetailView):
    model = Album

class AlbumUpload(ContextHackMixin, DetailView):
    model = Album
    template_name = "albuns/album_upload.html"

def _send_file(album, request):
    try:
        file = request.FILES['file']
        photo = Photo(content_object=album)
        print photo, type(photo.image)
        photo.image.save(file.name, file)

        photo.save()

    except Exception, e:
        return JSONResponse({'error': str(e)})
    else:
        photo = Photo.objects.get(id=photo.id) #fix bug :-|
        return JSONResponse({'error': None, 'id': photo.id, 'name': photo.name, 'url': photo.image.url,
                             'size': photo.image.size,
                         'thumbnail': photo.image.thumbnail.url()})

def _edit_image(album, request):
    photo_id = request.POST.get('photo_id', '')
    name = request.POST.get('name', '')

    if not photo_id:
        return JSONResponse({'error': 'necessario especificar o photo_id'})

    photo = get_object_or_404(Photo.objects.get_all_related(album),
                              id=int(photo_id))
    photo.name = name
    photo.save()

    return JSONResponse({'error': None, 'id': photo.id, 'name': photo.name, 'url': photo.image.url,
                         'thumburl': photo.image.thumbnail.url()})

def _delete_image(album, request):
    photo_id = request.POST.get('photo_id', '')

    if not photo_id:
        return JSONResponse({'error': 'necessario especificar o photo_id'})

    photo = get_object_or_404(Photo.objects.get_all_related(album),
                              id=int(photo_id))
    photo.delete_files()
    photo.delete()
    

    return JSONResponse({'error': None})

def _delete_album(request):
    album_id = request.POST.get('album_id', '')

    if not album_id:
        return JSONResponse({'error': 'necessario especificar o album_id'})

    album = get_object_or_404(Album, id=album_id)

    for photo in Photo.objects.get_all_related(album):
        photo.delete_files()
        photo.delete()

    album.delete()
    return JSONResponse({'error': None})

@login_required
def image_action(request, pk):
    album = get_object_or_404(Album, pk=pk)
    action = request.POST.get('action', '')
    
    if action == 'send_image':
        return _send_file(album, request)

    elif action == 'edit_image':
        return _edit_image(album, request)

    elif action == 'delete_image':
        return _delete_image(album, request)

    raise Http404

@login_required
def album_action(request):
    action = request.POST.get('action', '')
    
    if action == 'delete_album':
        return _delete_album(request)
    
    raise Http404

@login_required
def upload(request, pk):
    album = get_object_or_404(Album, pk=pk)
    return _send_file(album, request)
