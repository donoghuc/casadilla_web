import sys
import os
import datetime
import pkg_resources
from pyramid.config import Configurator

import casadilla_app
import casadilla_app.controllers.home_controller as home
from casadilla_app.services.log_service import LogService

dev_mode = False


def main(_, **settings):
    '''pull in configuration settings, initialize and fire off app server'''
    config = Configurator(settings=settings)

    init_logging(config)  # runs first
    init_mode(config)
    init_includes(config)
    init_routing(config)
    # init_db(config)

    return config.make_wsgi_app()


def init_logging(config):
    ''' specify loggin infor mation '''
    settings = config.get_settings()
    log_level = settings.get('log_level')
    log_filename = settings.get('log_filename')

    LogService.global_init(log_level, log_filename)

    log_package_versions()


# def init_db(_):
#     top_folder = os.path.dirname(casadilla_app.__file__)
#     rel_folder = os.path.join('db', 'blue_yellow.sqlite')

#     db_file = os.path.join(top_folder, rel_folder)
#     DbSessionFactory.global_init(db_file)


def init_mode(config):
    ''' dev mode for verbose output and stack tracing, prod for running on server'''
    global dev_mode
    settings = config.get_settings()
    dev_mode = settings.get('mode') == 'dev'
    print('Running in {} mode.'.format('dev' if dev_mode else 'prod'))


def init_routing(config):
    ''' declare routing information to map MVC'''
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_handler('root', '/', handler=home.HomeController, action='index')
    add_controller_routes(config, home.HomeController, 'home')
    config.scan()


def add_controller_routes(config, ctrl, prefix):
    ''' deal with case of trailing / and different routes. '''
    config.add_handler(prefix + 'ctrl_index', '/' + prefix, handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl_index/', '/' + prefix + '/', handler=ctrl, action='index')
    config.add_handler(prefix + 'ctrl', '/' + prefix + '/{action}', handler=ctrl)
    config.add_handler(prefix + 'ctrl/', '/' + prefix + '/{action}/', handler=ctrl)
    # config.add_handler(prefix + 'ctrl_id', '/' + prefix + '/{action}/{id}', handler=ctrl) # possibly remove this as no login yet


def init_includes(config):
    ''' using chameleon template and pyramid handlers'''
    config.include('pyramid_chameleon')
    config.include('pyramid_handlers')


def log_package_versions():
    startup_log = LogService.get_startup_log()

    # update from setup.py when changed!
    # This list is the closure of all dependencies,
    # taken from: pip list --format json
    requires = [{"name": "Chameleon"},
                {"name": "docopt", "version": "0.4.0"},
                {"name": "html2text", "version": "2016.9.19"},
                {"name": "hupper", "version": "0.4.1"}, {"name": "Logbook", "version": "1.0.0"},
                {"name": "mailchimp", "version": "2.0.9"}, {"name": "mailer", "version": "0.8.1"},
                {"name": "Mako", "version": "1.0.6"}, {"name": "MarkupSafe", "version": "0.23"},
                {"name": "passlib", "version": "1.7.0.post20170103083911"}, {"name": "PasteDeploy", "version": "1.5.2"},
                {"name": "pip", "version": "9.0.1"}, {"name": "Pygments", "version": "2.1.3"},
                {"name": "pyramid", "version": "1.8a1"}, {"name": "pyramid-chameleon", "version": "0.3"},
                {"name": "pyramid-debugtoolbar", "version": "3.0.5"}, {"name": "pyramid-handlers", "version": "0.5"},
                {"name": "pyramid-mako", "version": "1.0.2"}, {"name": "repoze.lru", "version": "0.6"},
                {"name": "requests", "version": "2.12.4"}, {"name": "setuptools", "version": "28.8.0"},
                {"name": "SQLAlchemy", "version": "1.1.4"}, {"name": "stripe", "version": "1.46.0"},
                {"name": "translationstring", "version": "1.3"}, {"name": "venusian", "version": "1.0"},
                {"name": "waitress", "version": "1.0.1"}, {"name": "WebOb", "version": "1.7.0"},
                {"name": "zope.deprecation", "version": "4.2.0"}, {"name": "zope.interface", "version": "4.3.3"}]

    requires.sort(key=lambda d: d['name'].lower())
    t0 = datetime.datetime.now()
    startup_log.notice('---------- Python version info ------------------')
    startup_log.notice(sys.version.replace('\n', ' ').replace('  ', ' '))
    startup_log.notice('---------- package version info ------------------')
    for rec in requires:
        try:
            version = pkg_resources.get_distribution(rec['name']).version
            if version:
                startup_log.notice('{} v{}'.format(rec['name'], version))
            else:
                startup_log.notice("WHERE IS IT? {}.".format(rec['name']))
        except Exception as x:
            startup_log.notice('{} UNKNOWN VERSION ({})'.format(rec['name'], x))

    dt = datetime.datetime.now() - t0

    startup_log.notice('Package info gathered in {} sec'.format(dt.total_seconds()))
    startup_log.notice('--------------------------------------------------')