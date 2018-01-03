from pyramid import testing
import pytest

@pytest.fixture
def pyramid_req():
	''' build fixture for setting up requests'''
	return testing.DummyRequest()