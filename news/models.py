from django.db import models
from django.contrib.auth.models import User
from stdimage import StdImageField

class Notice(models.Model):
    name = models.CharField("Nome", max_length=100)
    date = models.DateTimeField("Data", auto_now_add=True)
    text = models.TextField("Texto")
    user = models.ForeignKey(User)
    image = StdImageField("Foto", upload_to='news', size=(400, 300), thumbnail_size=(200, 200, True))

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ("-date",)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return unicode("/news/%d/" % self.id)
