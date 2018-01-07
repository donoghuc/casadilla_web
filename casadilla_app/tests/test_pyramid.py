from casadilla_app.controllers.home_controller import HomeController
from casadilla_app.controllers.meta_controller import MetaController


def test_home_index(pyramid_req):
	''' test response to request to /home '''
	response = HomeController.index(pyramid_req)
	assert response['value'] == 'HOME'


def test_home_index(pyramid_req):
	''' test response to request to /meta '''
	response = MetaController.index(pyramid_req)
	assert response['value'] == 'META'