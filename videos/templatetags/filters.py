from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django import template
import re

register = template.Library()
regex = re.compile(r"^(http://)?(www\.)?(youtube\.com/watch\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})")

@register.filter
@stringfilter
def youtubeurl(url):
    match = regex.match(url)
    if not match: return ""
    video_id = match.group('id')
    return mark_safe("http://www.youtube.com/embed/%s" % video_id)
youtubeurl.is_safe = True # Don't escape HTML

@register.filter
@stringfilter
def youtube(url):
    match = regex.match(url)
    if not match: return ""
    video_id = match.group('id')
    return mark_safe("""<iframe title="YouTube video player" width="320" height="240" src="http://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>""" % video_id)
youtube.is_safe = True # Don't escape HTML

@register.filter
@stringfilter
def youtubepreview(url):
    match = regex.match(url)
    if not match: return ""
    video_id = match.group('id')
    return mark_safe("""<img src="http://img.youtube.com/vi/%s/2.jpg"/>""" % video_id)
youtubepreview.is_safe = True # Don't escape HTML
