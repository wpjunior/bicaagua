from django.utils import simplejson
from django.http import HttpResponse
from django.template import RequestContext

class JSONResponse(HttpResponse):
    """ JSON response class """
    def __init__(self,content='',json_opts={},mimetype="application/json",*args,**kwargs):
        
        if content:
            content = simplejson.dumps(content,**json_opts)
        else:
            content = simplejson.dumps([],**json_opts)

        super(JSONResponse,self).__init__(content,mimetype,*args,**kwargs)

class ContextHackMixin(object):
    def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        context['request'] = self.request
        if hasattr(self, "get_extra_context"):
            context.update(self.get_extra_context())
            
        return self.response_class(
            request = self.request,
            template = self.get_template_names(),
            context = RequestContext(self.request, context),
            **response_kwargs
        )
