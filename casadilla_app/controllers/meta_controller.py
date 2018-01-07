import pyramid_handlers
from casadilla_app.controllers.base_controller import BaseController



class MetaController(BaseController):
    alternate_mode = False

    @pyramid_handlers.action(renderer='templates/meta/index.pt')
    def index(self):
        ''' display the main index page for the site and log when user hits it'''
        self.log.notice(self.req_details)
        return {'value': 'META'}


    def alternate_row_style(self):
        ''' alternate the class name of divs on home page view to handle differ  '''
        alt = self.alternate_mode
        self.alternate_mode = not self.alternate_mode

        if alt:
            return "alternate"
        else:
            return ""