import pytest
import requests
from helpers.helpers import Person
from data.urls import URL, Endpoints

@pytest.fixture
def create_new_user():
    user_data = Person.create_data_correct_user()
    response = requests.post(URL.main_url + Endpoints.CREATE_USER, data=user_data)
    yield user_data, response
    token = response.json()["accessToken"]
    requests.delete(URL.main_url + Endpoints.DELETE_USER, headers={"Authorization": token})

def pytest_make_parametrize_id(val):
    return repr(val)