from os.path import splitext
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import render_to_response
from hashlib import md5
from wikipages.models import Page, Photo
from wikipages.forms import PageForm
from utils import JSONResponse
DEFAULT_TEMPLATE = 'wikipages/page.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.

@csrf_protect
def wikipage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    if not url.startswith('/'):
        url = "/" + url

    if request.method == "GET":
        action = request.GET.get('action', '')

        if not action:
            action = request.POST.get('action', '') 

    else:
        action = request.POST.get('action', '')

        if not action:
            action = request.GET.get('action', '') 

    print request.method, request.POST, request.GET
        
    try:
        f = Page.objects.get(url__exact=url)
    except Page.DoesNotExist:
        f = None

    if action:
        if not request.user.is_authenticated():
            return redirect_to_login(request.path)
    else:
        if not f:
            if request.user.is_authenticated():
                return render_to_response("wikipages/404.html", locals(),
                                          context_instance=RequestContext(request))
            raise Http404
        return render_wikipage(request, f)
    
    if action == 'edit':
        if request.method == 'POST':
            if f:
                form = PageForm(request.POST, request.FILES, instance=f)
            else:
                form = PageForm(request.POST, request.FILES)

            if form.is_valid():
                obj = form.save(commit=False)
                obj.url = url
                obj.save()
                return HttpResponseRedirect(url)
        else:
            if f:
                form = PageForm(instance=f)
            else:
                form = PageForm()

        return render_to_response('wikipages/form.html',
                                  locals(),
                                  context_instance=RequestContext(request))


    
    if action == "send_image":
        file = request.FILES['file']
        contents = file.read()
        hash = md5(contents).hexdigest()
        b, ext = splitext(file.name)
        filename = "%s%s" %(hash, ext)

        if f is None:
            f = Page(url=url)
            f.save()

        p = Photo(content_object=f)
        p.image.save(filename, file)
        p.save()
        
        return JSONResponse({'url': p.image.url})
    #actions edit, delete
    raise Http404

@csrf_protect
def render_wikipage(request, f):
    """
    Internal interface to the wiki page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
        
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, {
        'page': f,
        'request': request,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, Page, f.id)
    return response
