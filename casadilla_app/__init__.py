from pyramid.config import Configurator
import os
import casadilla_app
import casadilla_app.controllers.home_controller as home
# import casadilla_app.controllers.albums_controller as albums
# import casadilla_app.controllers.account_controller as account
# import casadilla_app.controllers.admin_controller as admin
# import casadilla_app.controllers.newsletter_controller as news
# from casadilla_app.data.dbsession import DbSessionFactory
# from casadilla_app.email.template_paser import EmailTemplateParser
# from casadilla_app.services.email_service import EmailService
# from casadilla_app.services.mailinglist_service import MailingListService

dev_mode = False


def main(_, **settings):
    config = Configurator(settings=settings)

    init_mode(config)
    init_includes(config)
    init_routing(config)
    # init_db(config)

    return config.make_wsgi_app()



# def init_db(_):
#     top_folder = os.path.dirname(casadilla_app.__file__)
#     rel_folder = os.path.join('db', 'blue_yellow.sqlite')

#     db_file = os.path.join(top_folder, rel_folder)
#     DbSessionFactory.global_init(db_file)


def init_mode(config):
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
    print('Running in {} mode.'.format('dev' if dev_mode else 'prod'))



def init_routing(config):
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_handler('root', '/', handler=home.HomeController, action='index')

    add_controller_routes(config, home.HomeController, 'home')

    config.scan()


def add_controller_routes(config, ctrl, prefix):
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{id}', handler=ctrl) # possibly remove this as no login yet


def init_includes(config):
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')
