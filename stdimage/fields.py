from django.db.models.fields.files import ImageField
from django.db.models import signals
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from widgets import DelAdminFileWidget
from forms import StdImageFormField
import os, shutil
from PIL import Image, ImageOps
from bicaagua.settings import MEDIA_ROOT

def watermark(im, mark, position):
    """Adds a watermark to an image."""
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

class ThumbnailField:
    '''
    Instances of this class will be used to access data of the
    generated thumbnails
    '''
    def __init__(self, name):
        self.name = name
        self.storage = FileSystemStorage()

    def path(self):
        return self.storage.path(self.name)

    def url(self):
        return self.storage.url(self.name)

    def size(self):
        return self.storage.size(self.name)

class StdImageField(ImageField):
    '''
    Django field that behaves as ImageField, with some extra features like:
        - Auto resizing
        - Automatically generate thumbnails
        - Allow image deletion
    '''
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, size=None, thumbnail_size=None, **kwargs):
        '''
        Added fields:
            - size: a tuple containing width and height to resize image, and an optional boolean setting if is wanted forcing that size (None for not resizing).
                * Example: (640, 480, True) -> Will resize image to a width of 640px and a height of 480px. File will be cutted if necessary for forcing te image to have the desired size
            - thumbnail_size: a tuple with same values than `size' (None for not creating a thumbnail 
        '''
        params_size = ('width', 'height', 'force')
        for att_name, att in {'size': size, 'thumbnail_size': thumbnail_size}.items():
            if att and (isinstance(att, tuple) or isinstance(att, list)):
                setattr(self, att_name, dict(map(None, params_size, att)))
            else:
                setattr(self, att_name, None)
        super(StdImageField, self).__init__(verbose_name, name, width_field, height_field, **kwargs)

    def _get_thumbnail_filename(self, filename):
        '''
        Returns the thumbnail name associated to the standard image filename
            * Example: /var/www/myproject/media/img/picture_1.jpeg
                will return /var/www/myproject/media/img/picture_1.thumbnail.jpeg
        '''
        splitted_filename = list(os.path.splitext(filename))
        splitted_filename.insert(1, '.thumbnail')
        return ''.join(splitted_filename)

    def _resize_image(self, filename, size):
        '''
        Resizes the image to specified width, height and force option
            - filename: full path of image to resize
            - size: dictionary containing:
                - width: new width
                - height: new height
                - force: if True, image will be cropped to fit the exact size,
                    if False, it will have the bigger size that fits the specified
                    size, but without cropping, so it could be smaller on width or height
        '''
        WIDTH, HEIGHT = 0, 1
        
        img = Image.open(filename)
        mark = Image.open(MEDIA_ROOT + '/img/overlay.png')
        img = watermark(img, mark, (10, 10))
        img.save(filename)

        if img.size[WIDTH] > size['width'] or img.size[HEIGHT] > size['height']:
            if size['force']:
                img = ImageOps.fit(img, (size['width'], size['height']), Image.ANTIALIAS)
            else:
                img.thumbnail((size['width'], size['height']), Image.ANTIALIAS)
            
            try:
                img.save(filename, optimize=1)
            except IOError:
                img.save(filename)

    def _rename_resize_image(self, instance=None, **kwargs):
        '''
        Renames the image, and calls methods to resize and create the thumbnail
        '''
        if getattr(instance, self.name):
            filename = getattr(instance, self.name).path
            ext = os.path.splitext(filename)[1].lower().replace('jpg', 'jpeg')
            dst = self.generate_filename(instance, '%s_%s%s' % (self.name, instance._get_pk_val(), ext))
            dst_fullpath = os.path.join(settings.MEDIA_ROOT, dst)
            if os.path.abspath(filename) != os.path.abspath(dst_fullpath):
                os.rename(filename, dst_fullpath)
                if self.size:
                    self._resize_image(dst_fullpath, self.size)
                if self.thumbnail_size:
                    thumbnail_filename = self._get_thumbnail_filename(dst_fullpath)
                    shutil.copyfile(dst_fullpath, thumbnail_filename)
                    self._resize_image(thumbnail_filename, self.thumbnail_size)
                setattr(instance, self.attname, dst)
                instance.save()

    def _set_thumbnail(self, instance=None, **kwargs):
        '''
        Creates a "thumbnail" object as attribute of the ImageField instance
        Thumbnail attribute will be of the same class of original image, so
        "path", "url"... properties can be used
        '''
        if getattr(instance, self.name):
            filename = self.generate_filename(instance, os.path.basename(getattr(instance, self.name).path))
            thumbnail_filename = self._get_thumbnail_filename(filename)
            thumbnail_field = ThumbnailField(thumbnail_filename)
            setattr(getattr(instance, self.name), 'thumbnail', thumbnail_field)


    def formfield(self, **kwargs):
        '''
        Specify form field and widget to be used on the forms
        '''
        kwargs['widget'] = DelAdminFileWidget
        kwargs['form_class'] = StdImageFormField
        return super(StdImageField, self).formfield(**kwargs)

    def save_form_data(self, instance, data):
        '''
            Overwrite save_form_data to delete images if "delete" checkbox
            is selected
        '''
        if data == '__deleted__':
            filename = getattr(instance, self.name).path
            if os.path.exists(filename):
                os.remove(filename)
            thumbnail_filename = self._get_thumbnail_filename(filename)
            if os.path.exists(thumbnail_filename):
                os.remove(thumbnail_filename)
            setattr(instance, self.name, None)
        else:
            super(StdImageField, self).save_form_data(instance, data)

    def get_db_prep_save(self, value):
        '''
            Overwrite get_db_prep_save to allow saving nothing to the database
            if image has been deleted
        '''
        if value:    
            return super(StdImageField, self).get_db_prep_save(value)
        else:
            return u''

    def contribute_to_class(self, cls, name):
        '''
        Call methods for generating all operations on specified signals
        '''
        super(StdImageField, self).contribute_to_class(cls, name)
        signals.post_save.connect(self._rename_resize_image, sender=cls)
        signals.post_init.connect(self._set_thumbnail, sender=cls)

