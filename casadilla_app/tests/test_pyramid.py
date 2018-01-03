from casadilla_app.controllers.home_controller import HomeController


def test_home_index(pyramid_req):
	''' test response to request to / '''
	response = HomeController.index(pyramid_req)
	assert response['value'] == 'HOME'