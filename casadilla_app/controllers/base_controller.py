import logbook
import json
import pyramid.renderers
import pyramid.httpexceptions as exc

import casadilla_app.infrastructure.static_cache as static_cache
from casadilla_app.infrastructure.supressor import suppress


class BaseController:
    def __init__(self, request):
        self.request = request
        self.build_cache_id = static_cache.build_cache_id

        layout_render = pyramid.renderers.get_renderer('casadilla_app:templates/shared/_layout.pt')
        impl = layout_render.implementation()
        self.layout = impl.macros['layout']

        log_name = 'Ctrls/' + type(self).__name__.replace("Controller", "")
        self.log = logbook.Logger(log_name)


    @suppress()
    def redirect(self, to_url, permanent=False):
        ''' hide from navigation with supress decorator, NOTE: update with __autoexpose__'''
        if permanent:
            raise exc.HTTPMovedPermanently(to_url)
        raise exc.HTTPFound(to_url)


    @property
    def data_dict(self):
        ''' more request manipulation in base class '''
        data = dict()
        data.update(self.request.GET)
        data.update(self.request.POST)
        data.update(self.request.matchdict)

        return data


    @property
    def req_details(self):
        ''' gather interesting user details to log when hitting homepg  '''
        interesting_params = ['REMOTE_ADDR', 'HTTP_USER_AGENT', 'HTTP_REFERER', 'HTTP_COOKIE']
        return  json.dumps({key: self.request.headers.environ[key] for key in interesting_params})